import ffi
import uctypes

libc = None
try:
    libc = ffi.open("libc.so.6")
except:
    print("libc could not be found")


SIGABRT = 6
SIGALRM = 14
SIGBUS = 7
SIGCHLD = 17
SIGCONT = 18
SIGFPE = 8
SIGHUP = 1
SIGILL = 4
SIGINT = 2
SIGKILL = 9
SIGPIPE = 13
SIGQUIT = 3
SIGSEGV = 11
SIGSTOP = 19
SIGTERM = 15
SIGTSTP = 20
SIGTTIN = 21
SIGTTOU = 22
SIGUSR1 = 10
SIGUSR2 = 12
SIGPOLL = 29
SIGPROF = 27
SIGSYS = 31
SIGTRAP = 5
SIGURG = 23
SIGVTALRM = 26
SIGXCPU = 24
SIGXFSZ = 25


O_RDONLY = 0
O_WRONLY = 1
O_RDWR = 2

I2C_SLAVE = 1795


if libc:
    perror = libc.func("v", "perror", "s")
    popen = libc.func("p", "popen", "ss")
    pclose = libc.func("i", "pclose", "s")
    fopen = libc.func("p", "fopen", "ss")
    fclose = libc.func("i", "fclose", "s")
    fwrite = libc.func("i", "fwrite", "PiiP")
    fgets = libc.func("s", "fgets", "sis")
    fflush = libc.func("i", "fflush", "s")
    errno = libc.var("i", "errno")
    kill = libc.func("i", "kill", "ii")
    waitpid = libc.func("i", "waitpid", "iii")
    fork = libc.func("i", "fork", "")
    execv = libc.func("i", "execv", "ss")
    setenv = libc.func("i", "setenv", "ssi")

    open = libc.func("p", "open", "si")
    ioctl = libc.func("p", "ioctl", "iii")
    write = libc.func("p", "write", "isi")
    read = libc.func("p", "read", "isi")

    


    def runShellCommand(cmd):
        strbuffer = " " * 256
        fp = popen(cmd, "re")
        output = ""

        while( fgets(strbuffer, len(strbuffer), fp) != None):
            line = str(strbuffer)
            output += (line.rstrip().replace("\x00", ""))
            strbuffer = " " * 256

        ret = pclose(fp)
        if(ret != 0):
            print("error closing pipe: ", ret)
        return output.rstrip()

else:
    def runShellCommand(cmd):
        print(cmd)
