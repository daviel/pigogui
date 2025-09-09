import uasyncio as asyncio
import uos, time

# ---------- Public API ----------

def runShellCommand_bg(cmd: str, on_line=print, timeout_ms: int | None = None):
    loop = asyncio.get_event_loop()
    runner = _BgRunner(cmd, on_line=on_line, timeout_ms=timeout_ms)
    task = loop.create_task(runner._run())   # im Event-Loop starten
    return BgHandle(runner, task)

# ---------- Internals ----------

class BgHandle:
    def __init__(self, runner, task):
        self._runner = runner
        self._task = task

    def done(self) -> bool:
        return self._task.done()

    def result(self) -> int:
        # Exit-Code
        return self._task.result()

    def cancel(self):
        self._runner._request_cancel()

    @property
    def pid(self) -> int | None:
        return self._runner.pid

class _BgRunner:
    def __init__(self, cmd, on_line, timeout_ms):
        self.cmd = cmd
        self.on_line = on_line
        self.timeout_ms = timeout_ms
        self.base = str(time.ticks_us())
        self.out_path = f"/tmp/bg_{self.base}.out"
        self.pid_path = f"/tmp/bg_{self.base}.pid"
        self.rc_path  = f"/tmp/bg_{self.base}.rc"
        self.pid = None
        self._cancel_req = False

    def _request_cancel(self):
        self._cancel_req = True

    async def _run(self) -> int:
        for p in (self.out_path, self.pid_path, self.rc_path):
            try: uos.remove(p)
            except OSError: pass

        shell = (
            f"sh -c '"
            f"({self.cmd}) > {self.out_path} 2>&1 & "
            f"child=$!; echo $child > {self.pid_path}; "
            f"wait $child; echo $? > {self.rc_path}"
            f"'"
        )
        uos.system(shell + " &")

        start_ticks = time.ticks_ms()
        while self.pid is None:
            self.pid = _try_read_int(self.pid_path)
            if self.pid is not None:
                break
            await asyncio.sleep_ms(10)
            if time.ticks_diff(time.ticks_ms(), start_ticks) > 2000:
                raise RuntimeError("Konnte PID nicht ermitteln")

        rc = await self._tail_and_wait(self.pid, start_ticks)
        for p in (self.pid_path,):
            try: uos.remove(p)
            except OSError: pass
        return rc

    async def _tail_and_wait(self, pid: int, start_ticks: int) -> int:
        pos = 0
        partial = b""
        last_size = 0

        while True:
            try:
                size = uos.stat(self.out_path)[6]
            except OSError:
                size = 0
            if size != last_size or size > pos:
                try:
                    with open(self.out_path, "rb") as f:
                        f.seek(pos)
                        chunk = f.read()
                    if chunk:
                        pos += len(chunk)
                        partial += chunk
                        while True:
                            nl = partial.find(b"\n")
                            if nl < 0:
                                break
                            line = partial[:nl]
                            partial = partial[nl+1:]
                            try:
                                self.on_line(line.decode("utf-8", "ignore"))
                            except Exception:
                                pass
                except OSError:
                    pass
                last_size = size

            if self.timeout_ms is not None:
                if time.ticks_diff(time.ticks_ms(), start_ticks) > self.timeout_ms:
                    await self._terminate(pid, grace_ms=800)
                    return self._final_rc(default_rc=124)

            if self._cancel_req:
                await self._terminate(pid, grace_ms=800)
                return self._final_rc(default_rc=130)

            if not _is_alive(pid):
                if partial:
                    try: self.on_line(partial.decode("utf-8", "ignore"))
                    except Exception: pass
                    partial = b""
                return self._final_rc(default_rc=0)

            await asyncio.sleep_ms(40)

    async def _terminate(self, pid: int, grace_ms: int = 800):
        uos.system(f"kill -TERM {pid} >/dev/null 2>&1")
        t0 = time.ticks_ms()
        while _is_alive(pid) and time.ticks_diff(time.ticks_ms(), t0) < grace_ms:
            await asyncio.sleep_ms(40)
        if _is_alive(pid):
            uos.system(f"kill -KILL {pid} >/dev/null 2>&1")

    def _final_rc(self, default_rc: int) -> int:
        rc = _try_read_int(self.rc_path)
        if rc is None:
            rc = default_rc
        try: uos.remove(self.rc_path)
        except OSError: pass
        return rc


def _try_read_int(path: str):
    try:
        with open(path, "rb") as f:
            s = f.read().strip()
        if not s:
            return None
        n = 0
        neg = False
        i = 0
        if s and s[0:1] == b'-':
            neg = True; i = 1
        while i < len(s) and 48 <= s[i] <= 57:  # '0'..'9'
            n = n * 10 + (s[i] - 48)
            i += 1
        return -n if neg else n
    except OSError:
        return None
    except Exception:
        return None

def _is_alive(pid: int) -> bool:
    rc = uos.system(f"kill -0 {pid} >/dev/null 2>&1")
    return rc == 0
