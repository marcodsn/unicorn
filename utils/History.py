class History:
    def __init__(self, k=2):
        self.k = k
        self.history = []

    def add(self, message, retrieved, answer):
        self.history.append("<|user|>" + message + ("<|retrieved|>" + retrieved) if retrieved != None else "" + "<|model|>" + answer)
        if len(self.history) > self.k:
            self.history.pop(0)

    def get(self):
        history_out = ""
        for i in range(len(self.history)):
            history_out += self.history[i]
        return history_out