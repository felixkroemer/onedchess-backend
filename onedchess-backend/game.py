import datetime
import random
import string
import json


class Game():

    def __init__(self):
        self._app = None
        self._socket = None
        self._idleIDs = {}
        self._games = {}
        return

    def init(self, app, socket):
        self._app = app
        self._socket = socket
        return

    def createID(self):
        self.cleanIDs()
        tries = 0
        while True:
            id = ''.join([random.choice(string.ascii_uppercase)
                          for i in range(5)])
            if not self.hasID(id):
                self._idleIDs[id] = datetime.datetime.now()
                return id
            tries += 1
            if tries >= 20:
                return None

    def hasID(self, id):
        if id in self._idleIDs:
            return True
        else:
            return False

    def cleanIDs(self):
        now = datetime.datetime.now()
        for x in self._idleIDs:
            diff = now - self._idleIDs[x]
            if(diff.days > 0 or diff.seconds > 1200):
                del self._idleIDs[x]
        self._lastCleanup = now

    def createGame(self, playerID, partnerID):
        if(playerID in self._idleIDs and partnerID in self._idleIDs):
            self._idleIDs.pop(playerID)
            self._idleIDs.pop(partnerID)
            self._games[(playerID, partnerID)] = {"playerTurn": True}
            self._socket.emit('startGame', json.dumps(
                {"white": playerID, "black": partnerID}))
            return True
        else:
            return False
