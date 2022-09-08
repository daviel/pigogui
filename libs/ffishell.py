import ffi
import uctypes

libc = ffi.open("libc.so.6")


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


perror = libc.func("v", "perror", "s")
popen = libc.func("p", "popen", "ss")
pclose = libc.func("i", "pclose", "s")
fgets = libc.func("s", "fgets", "sis")
fflush = libc.func("i", "fflush", "s")
errno = libc.var("i", "errno")
kill = libc.func("v", "kill", "ii")




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