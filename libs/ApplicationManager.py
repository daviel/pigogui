from libs.ffishell import runShellCommand
from libs.init_drv import addGlobalKeyCallback
import libs.Singletons as SINGLETONS
from libs.Helper import SDL_KEYS

class ApplicationManager:
    main_app = -1
    app_call = ""
    app_keymap = ""
    is_paused = False


    def __init__(self):
        addGlobalKeyCallback(self.triggerQuickMenu)
        self.setKeyMap()

    def startApp(self, app, keymap=""):
        print("nohup " + app + " &")
        self.app_call = app
        self.setKeyMap(keymap)
        self.app_keymap = keymap
        self.main_app = runShellCommand("nohup " + app + " & echo $!")
        print("PID: " + self.main_app)
        SINGLETONS.PAGE_MANAGER.hideCurrentPage()

    def stopMainApp(self):
        runShellCommand("kill " + self.main_app)
        self.app_call = ""
        self.main_app = -1
        self.setKeyMap()
        SINGLETONS.PAGE_MANAGER.showCurrentPage()

    def pauseMainApp(self):
        self.is_paused = True
        runShellCommand("pkill -P -STOP " + self.main_app)
        self.setKeyMap()
        
    def resumeMainApp(self):
        self.is_paused = False
        runShellCommand("pkill -P -CONT " + self.main_app)
        self.setKeyMap(self.app_keymap)

    def triggerQuickMenu(self, indev, drv, data):
        print(indev.get_key())
        if indev.get_key() == SDL_KEYS["SDLK_DELETE"]:
            if(self.main_app != -1 and self.is_paused == False):
                print("show quickmenu")
                self.pauseMainApp()
                SINGLETONS.PAGE_MANAGER.showCurrentPage()
            elif self.main_app != -1 and self.is_paused == True:
                print("hide quickmenu")
                self.resumeMainApp()
                SINGLETONS.PAGE_MANAGER.hideCurrentPage()

    def setKeyMap(self, keymap=""):
        config = SINGLETONS.DATA_MANAGER.get("configuration")
        runShellCommand("sudo killall python")
        if keymap == "":
            keymap = config["defaultKeyMap"]
        keymap = keymap + " " + config["mandatoryKeyMap"]
        
        runShellCommand("nohup sudo python " + config["keymapperpath"] + " " + keymap + " &")
