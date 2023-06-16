import os
import json

from utils.History import History

class User:
    def __init__(self, id):
        self.id = id
        self.history = History()
        self.doc = None
        self.debug = False

    async def log(self, message, answer): # TODO: Add retrieved
        if not os.path.exists('logs'):
            os.mkdir('logs')
        if not os.path.exists('logs/' + str(self.id) + '.json'):
            f = open('logs/' + str(self.id) + '.json', 'w')
            json.dump([], f)
            f.close()
        f = open('logs/' + str(self.id) + '.json', 'r')
        data = json.load(f)
        f.close()
        f = open('logs/' + str(self.id) + '.json', 'w')
        data.append({'message': message, 'answer': answer})
        json.dump(data, f)
        f.close()
