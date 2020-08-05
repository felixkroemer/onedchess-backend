import datetime
import random
import string


class Game():

    def __init__(self):
        self._app = None
        self._idleIDs = []
        return

    def init(self, app):
        self._app = app
        return

    def createID(self):
        self.cleanIDs()
        tries = 0
        while True:
            id = ''.join([random.choice(string.ascii_uppercase)
                          for i in range(5)])
            if not self.hasID(id):
                self._idleIDs.append((id, datetime.datetime.now()))
                return id
            tries += 1
            if tries >= 20:
                return None

    def hasID(self, id):
        for x in self._idleIDs:
            if id in x:
                return True
        return False

    def cleanIDs(self):
        now = datetime.datetime.now()
        for x in self._idleIDs:
            diff = now - x[1]
            if(diff.days > 0 or diff.seconds > 600):
                self._idleIDs.remove(x)
        self._lastCleanup = now
