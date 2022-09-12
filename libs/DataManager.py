#from data.games import games
import io
import json

class DataManager:
    data = {}

    def __init__(self):
        self.load("./data/games.json", "games")
        self.save("./data/games1.json", self.data['games'])
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
