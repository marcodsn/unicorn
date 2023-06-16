from utils.User import User

class UsersManager:
    def __init__(self):
        self.users = {}

    def get(self, id):
        if id in self.users:
            return self.users[id]
        else:
            self.users[id] = User(id)
            return self.users[id]

    def remove(self, id):
        if id in self.users:
            del self.users[id]
