#from data.games import games
import io
import json
import os
from libs.GenericManager import GenericManager
import time
import lvgl as lv

from libs.ffishell import runShellCommand
from libs.threading import runShellCommand_bg

class DataManager(GenericManager):
    def __init__(self, singletons):
        self.data = {}
        self.fileJSONMap = {}
        self.updateAvailableCallbacks = []
        self.setSingletons(singletons)

        try:
            print("loading current configuration")
            self.load("./data/configuration.json", "configuration")
            self.load("./data/pigo.json", "pigo")
            self.load("./data/store.json", "store")
            self.updateConfigDefaults()
        except Exception:
            print("error loading config. Restoring defaults")
            self.load("./data/configurationDefault.json", "configuration")
            self.fileJSONMap["configuration"] = "./data/configuration.json"
            self.saveAll()
        
        self.findGames(self.get("configuration")["gamesdir"])
        config = self.get("configuration")
        if config["debug"] == False:
            self.checkForUpdate()
        pass

    def loadJSON(self, filename):
        file = io.open(filename, 'r')
        content = file.readlines()
        jsonContent = json.loads(' '.join(map(str, content)))
        file.close()
        return jsonContent

    def load(self, filename, key):
        file = io.open(filename, 'r')
        content = file.readlines()
        self.data[key] = json.loads(' '.join(map(str, content)))
        file.close()
        self.fileJSONMap[key] = filename

    def updateConfigDefaults(self):
        defaults = self.loadJSON("./data/configurationDefault.json")
        newConf = self.merge(defaults, self.data["configuration"])
        self.data["configuration"] = newConf
        pass

    def merge(self, a: dict, b: dict, path=[]):
        for key in b:
            if key in a:
                if isinstance(a[key], dict) and isinstance(b[key], dict):
                    self.merge(a[key], b[key], path + [str(key)])
                elif a[key] != b[key]:
                    a[key] = b[key]
            else:
                a[key] = b[key]
        return a

    def save(self, filename, content):
        file = io.open(filename, 'w')
        content = file.write(self.makeReadable(json.dumps(content)))
        file.close()
        pass

    def saveAll(self):
        for key in self.fileJSONMap:
            if key == "configuration":
                content = self.get(key)
                filename = self.fileJSONMap[key]
                self.save(filename, content)

    def get(self, key):
        return self.data[key]
    
    def makeReadable(self, content):
        return content.replace(",", ",\n").replace("{", "{\n").replace("}", "}\n")

    def findGames(self, dir):
        self.data["games"] = []
        gamesdir = self.get("configuration")["gamesdir"]

        for entry in os.ilistdir(dir):
            entry_type = entry[1]
            if entry_type == 0x4000: # check if dir
                dirname = entry[0]
                gameDir = gamesdir + "/" + dirname
                gameJson = gameDir + "/game.json"
                try:
                    os.stat(gameJson)
                except OSError:
                    continue
                print("game.json found ", gameDir)
                file = io.open(gameJson, 'r')
                content = file.readlines()
                file.close()

                game = json.loads(' '.join(map(str, content)))
                game["dirname"] = dirname
                game["main_image"] = gameDir + "/" + game["main_image"]
                game["small_image"] = gameDir + "/" + game["small_image"]

                for i in range(len(game["screenshots"])):
                    game["screenshots"][i] = gameDir + "/" + game["screenshots"][i]

                self.data["games"].append(game)

    def checkForUpdate(self):
        t = time.localtime()
        year, month, day, hour, minute, second = t[0], t[1], t[2], t[3], t[4], t[5]
        date = f"{year:04d}-{month:02d}-{day:02d} {hour:02d}:{minute:02d}"
        config = self.get("configuration")
        config["user"]["system"]["updateCheckDate"] = date
        self.saveAll()
        self.handle = runShellCommand_bg("git fetch --quiet", on_done=self.checkForUpdateDone)

    def checkForUpdateDone(self, rc):
        ret = runShellCommand('git rev-list --count --left-right @{u}...HEAD')
        gitret = ret.split("\t")
        config = self.get("configuration")
        if gitret[0] != "0":
            self.singletons["NOTIFICATION_MANAGER"].add(lv.SYMBOL.UPLOAD, "New update available.")
            config["user"]["system"]["updateAvailable"] = True
        else:
            config["user"]["system"]["updateAvailable"] = False
        self.saveAll()
        for func in self.updateAvailableCallbacks:
            func(config["user"]["system"]["updateAvailable"])
    
    def updateAvailable(self):
        return self.get("configuration")["user"]["system"]["updateAvailable"]