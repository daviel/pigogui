#from data.games import games
import io
import json
import os

import libs.Singletons as SINGLETONS

class DataManager:
    data = {}

    def __init__(self):
        self.load("./data/configuration.json", "configuration")
        self.load("./data/store.json", "store")
        #self.save("./data/games1.json", self.data['games'])
        self.findGames(self.get("configuration")["gamesdir"])
        pass

    def load(self, filename, key):
        file = io.open(filename, 'r')
        content = file.readlines()
        self.data[key] = json.loads(' '.join(map(str, content)))
        file.close()

    def save(self, filename, content):
        file = io.open(filename, 'rw')
        content = file.write(json.dumps(content))
        file.close()
        pass

    def get(self, key):
        return self.data[key]

    def findGames(self, dir):
        self.data["games"] = []
        gamesdir = self.get("configuration")["gamesdir"]

        for dir in os.ilistdir(dir):
            type = dir[1]
            if type == 0x4000: # check if dir
                dirname = dir[0]
                print(dirname)
                gameDir = gamesdir + "/" + dirname
                gameJson = gameDir + "/game.json"
                if(os.stat(gameJson)):
                    print("game.json found")
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
        print(self.data["games"])
