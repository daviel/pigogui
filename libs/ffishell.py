import ffi
import uctypes

libc = ffi.open("libc.so.6")


perror = libc.func("v", "perror", "s")
popen = libc.func("p", "popen", "ss")
pclose = libc.func("i", "pclose", "s")
fgets = libc.func("s", "fgets", "sis")

errno = libc.var("i", "errno")

strbuffer = " " * 128


def runShellCommand(cmd):
    fp = popen(cmd, "r")
    strbuffer = " " * 128
    output = ""
    while( fgets(strbuffer, len(strbuffer), fp) != None):
        #print(strbuffer)
        line = str(strbuffer)
        output += (line.rstrip().replace("\x00", ""))
    ret = pclose(fp)

    return output
