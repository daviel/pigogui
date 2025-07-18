#from data.games import games
import io
import json
import os


class DataManager:
    data = {}
    fileJSONMap = {}

    def __init__(self):
        try:
            print("loading current configuration")
            self.load("./data/configuration.json", "configuration")
            self.updateConfigDefaults()
        except:
            print("error loading config. Restoring defauls")
            self.load("./data/configurationDefault.json", "configuration")
            self.fileJSONMap["configuration"] = "./data/configuration.json"

        #self.load("./data/store.json", "store")
        #self.save("./data/games1.json", self.data['games'])
        self.findGames(self.get("configuration")["gamesdir"])
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
        file = io.open(filename, 'rw')
        content = file.write(self.makeReadable(json.dumps(content)))
        file.close()
        pass

    def saveAll(self):
        for key in self.fileJSONMap:
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

        for dir in os.ilistdir(dir):
            type = dir[1]
            if type == 0x4000: # check if dir
                dirname = dir[0]
                gameDir = gamesdir + "/" + dirname
                gameJson = gameDir + "/game.json"
                if(os.stat(gameJson)):
                    print("game.json found ", gameDir)
                    file = io.open(gameJson, 'r')
                    content = file.readlines()
                    
                    game = json.loads(' '.join(map(str, content)))
                    game["dirname"] = dirname
                    game["main_image"] = gameDir + "/" + game["main_image"]
                    game["small_image"] = gameDir + "/" + game["small_image"]

                    for i in range(len(game["screenshots"])):
                        game["screenshots"][i] = gameDir + "/" + game["screenshots"][i]

                    self.data["games"].append(game)
                    file.close()
