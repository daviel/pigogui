import ffi
import uctypes

libc = ffi.open("libc.so.6")


perror = libc.func("v", "perror", "s")
popen = libc.func("p", "popen", "ss")
pclose = libc.func("i", "pclose", "s")
fgets = libc.func("s", "fgets", "sis")
fflush = libc.func("i", "fflush", "s")
errno = libc.var("i", "errno")

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
