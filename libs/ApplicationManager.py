from libs.ffishell import runShellCommand, kill, waitpid, fork, execv, SIGSTOP, SIGCONT, setenv, SIGKILL
from libs.init_drv import addGlobalKeyCallback
import libs.Singletons as SINGLETONS
from libs.Helper import SDL_KEYS
import array
import uctypes

class ApplicationManager:
    main_app_pid = -1
    app_call = ""
    app_keymap = ""
    keymap_pid = -1

    is_paused = False
    key_pressed = 0


    def __init__(self):
        addGlobalKeyCallback(self.triggerQuickMenu)
        self.setKeyMap()

    def startApp(self, app, keymap=""):
        print("nohup " + app + " &")
        self.stopMainApp()
        self.app_call = app
        self.setKeyMap(keymap)
        self.app_keymap = keymap
        self.main_app_pid = fork()
        if(self.main_app_pid == 0):
            ret = setenv("SDL_RPI_VIDEO_LAYER", "10", 1)
            print(ret)
            execv(app, None)
        print("PID: " + str(self.main_app_pid))
        SINGLETONS.PAGE_MANAGER.hideCurrentPage()

    def stopMainApp(self):
        if self.main_app_pid != -1:
            ret = kill(self.main_app_pid, SIGKILL)
            print(ret)
            waitpid(self.main_app_pid, None, 0)
            self.app_call = ""
            self.main_app_pid = -1
            self.setKeyMap()

    def pauseMainApp(self):
        self.is_paused = True
        ret = kill(self.main_app_pid, SIGSTOP)
        print(ret)
        self.setKeyMap()
        
    def resumeMainApp(self):
        self.is_paused = False
        ret = kill(self.main_app_pid, SIGCONT)
        print(ret)
        self.setKeyMap(self.app_keymap)

    def triggerQuickMenu(self, indev, drv, data):
        if self.main_app_pid != -1 and indev.get_key() == SDL_KEYS["SDLK_DELETE"]:
            self.key_pressed += 1
            if self.is_paused == True and self.key_pressed % 2 == 1:
                print("hide quickmenu")
                self.resumeMainApp()
                SINGLETONS.PAGE_MANAGER.hideCurrentPage()
            elif self.is_paused == False:
                print("show quickmenu")
                self.pauseMainApp()
                SINGLETONS.PAGE_MANAGER.showCurrentPage()
                self.key_pressed -= 1

    def setKeyMap(self, keymap=""):
        config = SINGLETONS.DATA_MANAGER.get("configuration")
        if self.keymap_pid != -1:
            kill(self.keymap_pid, SIGKILL)

        if keymap == "":
            keymap = config["defaultKeyMap"]
        keymap = keymap + " " + config["mandatoryKeyMap"]
        
        self.keymap_pid = fork()
        if(self.keymap_pid == 0):
            print("/usr/bin/python", config["keymapperpath"] + " " + keymap)
            
            args = array.array("L")
            args.append(uctypes.addressof(b'python'))
            args.append(uctypes.addressof(bytearray(config["keymapperpath"])))
            for key in keymap.split(" "):
                args.append(uctypes.addressof(bytearray(key)))
            
            ret = execv("/usr/bin/python", args)
        else:
            print(self.keymap_pid)
        