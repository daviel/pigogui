# uplayer.py
# Minimalistic audio player library for MicroPython (Unix port) on Linux.
# Uses existing CLI players (ffplay, mpg123, aplay, paplay, cvlc).
# Control is done via shell commands & POSIX signals (kill).

try:
    import uos as os  # MicroPython
except ImportError:
    import os         # fallback for CPython (e.g. for testing)

class AudioError(Exception):
    pass

class AudioManager:
    _CANDIDATES = ("ffplay", "mpg123", "aplay", "paplay", "cvlc")

    def __init__(self, preferred=None):
        """
        preferred: optional name of the desired player, e.g. "ffplay".
        """
        self.player = None
        self.pid = None
        self.last_cmd = None
        self.player = self._find_player(preferred)

    # ---------- Utility ----------

    def _sh(self, cmd):
        """Execute a shell command and return the exit code."""
        return os.system(cmd)

    def _which(self, cmd):
        return self._sh("which {} >/dev/null 2>&1".format(cmd)) == 0

    def _find_player(self, preferred):
        if preferred:
            if self._which(preferred):
                return preferred
            raise AudioError("Preferred player '{}' not found.".format(preferred))
        for c in self._CANDIDATES:
            if self._which(c):
                return c
        raise AudioError("No supported audio player installed "
                         "(ffplay/mpg123/aplay/paplay/cvlc).")

    def _build_cmd(self, filepath, loop=False):
        # Build a command line for a given player
        p = self.player
        if p == "ffplay":
            base = "ffplay -nodisp -autoexit -hide_banner -loglevel quiet '{}'".format(filepath)
        elif p == "mpg123":
            base = "mpg123 -q '{}'".format(filepath)
        elif p == "aplay":
            base = "aplay -q '{}'".format(filepath)
        elif p == "paplay":
            base = "paplay '{}'".format(filepath)
        elif p == "cvlc":
            base = "cvlc --play-and-exit --quiet '{}'".format(filepath)
        else:
            raise AudioError("Unknown player: {}".format(p))

        if loop:
            # Simple infinite loop via shell
            return "sh -c 'while :; do {}; done'".format(base)
        return base

    def _start_background(self, cmd):
        """
        Start a command in the background and store its PID.
        Uses /bin/sh to reliably capture the PID.
        """
        pidfile = "/tmp/uplayer_{}.pid".format(id(self))
        print(pidfile)
        start = "sh -c 'setsid {} >/dev/null 2>&1 & echo $! > {}'".format(cmd, pidfile)
        rc = self._sh(start)
        if rc != 0:
            raise AudioError("Could not start player (rc={}).".format(rc))

        # Read PID from temp file
        try:
            with open(pidfile, "r") as f:
                pid_s = f.read().strip()
        except Exception as e:
            raise AudioError("PID file could not be read: {}".format(e))

        try:
            os.remove(pidfile)
        except:
            pass

        try:
            self.pid = int(pid_s)
        except:
            self.pid = None
            raise AudioError("Invalid PID: '{}'".format(pid_s))

        self.last_cmd = cmd

    def _ensure_pid(self):
        if not self.pid:
            raise AudioError("No active playback process.")

    # ---------- Public API ----------

    def play(self, filepath, loop=False, blocking=False):
        """
        Play an audio file.
        - loop: True for infinite loop
        - blocking: True = wait until finished; False = background playback
        """
        self.stop(silent=True)  # stop any existing playback
        cmd = self._build_cmd(filepath, loop=loop)

        if blocking:
            rc = self._sh(cmd)
            if rc != 0:
                raise AudioError("Playback error (rc={}).".format(rc))
            self.pid = None
            self.last_cmd = None
        else:
            self._start_background(cmd)

    def pause(self):
        """Pause playback using SIGSTOP."""
        self._ensure_pid()
        self._sh("kill -STOP {}".format(self.pid))

    def resume(self):
        """Resume playback using SIGCONT."""
        self._ensure_pid()
        self._sh("kill -CONT {}".format(self.pid))

    def stop(self, silent=False):
        """Stop the current playback process."""
        if not self.pid:
            if not silent:
                raise AudioError("Nothing to stop.")
            return
        self._sh("kill {}".format(self.pid))
        self._sh("kill -0 {} >/dev/null 2>&1 || true".format(self.pid))
        self._sh("kill -KILL {} >/dev/null 2>&1 2>/dev/null || true".format(self.pid))
        self.pid = None
        self.last_cmd = None

    def is_playing(self):
        """Return True if process is still alive."""
        if not self.pid:
            return False
        return self._sh("kill -0 {} >/dev/null 2>&1".format(self.pid)) == 0

    def set_volume(self, percent):
        """
        Set the volume of the default sink via PulseAudio/PipeWire (pactl).
        Example: set_volume(50) -> 50%
        Requires 'pactl' and a running audio session.
        """
        if percent < 0:
            percent = 0
        cmd = "pactl set-sink-volume @DEFAULT_SINK@ {}%".format(percent)
        rc = self._sh(cmd)
        if rc != 0:
            raise AudioError("Could not set volume (pactl rc={}).".format(rc))

    def ensure_player(self, name):
        """
        Switch to another player if installed (e.g. 'ffplay' or 'mpg123').
        """
        if not self._which(name):
            raise AudioError("Player '{}' not found.".format(name))
        self.player = name

    def info(self):
        """Return a small status summary."""
        return {
            "player": self.player,
            "pid": self.pid,
            "playing": self.is_playing(),
            "last_cmd": self.last_cmd,
        }
