from libs.ffishell import *
from libs.init_drv import addGlobalKeyCallback
from libs.Helper import SDL_KEYS
import array
import uctypes
from libs.Singletons import *


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
        if app != self.app_call:
            print("nohup " + app + " &")
            self.stopMainApp()
            self.app_call = app
            self.main_app_pid = fork()
            if(self.main_app_pid == 0):
                ret = setenv("SDL_RPI_VIDEO_LAYER", "10", 1)
                print(ret)
                #execv(app, None)
            print("PID: " + str(self.main_app_pid))
        else:
            self.resumeMainApp()

        self.setKeyMap(keymap)
        self.app_keymap = keymap
        PAGE_MANAGER.hideCurrentPage()

    def stopMainApp(self):
        if self.main_app_pid != -1:
            print("killing pid: ", self.main_app_pid)
            ret = kill(self.main_app_pid, SIGKILL)
            waitpid(self.main_app_pid, None, 0)
            self.app_call = ""
            self.main_app_pid = -1
            self.setKeyMap()

    def pauseMainApp(self):
        print("pausing pid: ", self.main_app_pid)
        self.is_paused = True
        ret = kill(self.main_app_pid, SIGSTOP)
        self.setKeyMap()
        
    def resumeMainApp(self):
        print("resuming pid: ", self.main_app_pid)
        self.is_paused = False
        ret = kill(self.main_app_pid, SIGCONT)
        self.setKeyMap(self.app_keymap)

    def triggerQuickMenu(self, indev, drv, data):
        if self.main_app_pid != -1 and indev.get_key() == SDL_KEYS["SDLK_DELETE"]:
            self.key_pressed += 1
            if self.is_paused == True and self.key_pressed % 2 == 1:
                print("hide quickmenu")
                self.resumeMainApp()
                PAGE_MANAGER.hideCurrentPage()
            elif self.is_paused == False:
                print("show quickmenu")
                self.pauseMainApp()
                PAGE_MANAGER.showCurrentPage()
                self.key_pressed -= 1

    def setKeyMap(self, keymap=""):
        config = DATA_MANAGER.get("configuration")
        if self.keymap_pid != -1:
            kill(self.keymap_pid, SIGKILL)

        if keymap == "":
            keymap = config["defaultKeyMap"]
        keymap = keymap + " " + config["mandatoryKeyMap"]
        
        self.keymap_pid = fork()
        if(self.keymap_pid == 0):
            #print("/usr/bin/python", config["keymapperpath"] + " " + keymap)
            
            args = array.array("L")
            args.append(uctypes.addressof(bytes('python', 'utf8')))
            args.append(uctypes.addressof(bytearray(config["keymapperpath"], 'utf8')))
            for key in keymap.split(" "):
                args.append(uctypes.addressof(bytearray(key, 'utf8')))
            
            #ret = execv("/usr/bin/python", args)
        #else:
        #    print(self.keymap_pid)
        
