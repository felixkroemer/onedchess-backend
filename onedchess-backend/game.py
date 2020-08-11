import datetime
import random
import string
from .player import Player


class Game():

    def __init__(self):
        self._socket = None
        self._idleIDs = {}
        return

    def init(self, app, socket):
        self._socket = socket
        return

    def createID(self):
        self.cleanIDs()
        tries = 0
        while True:
            id = ''.join([random.choice(string.ascii_uppercase)
                          for i in range(5)])
            if not self.hasID(id):
                self._idleIDs[id] = Player(datetime.datetime.now())
                return id
            tries += 1
            if tries >= 20:
                return None

    def hasID(self, id):
        return id in self._idleIDs

    def cleanIDs(self):
        now = datetime.datetime.now()
        for x in self._idleIDs.copy():
            diff = now - self._idleIDs[x].dt
            if(diff.days > 0 or diff.seconds > 1200):
                del self._idleIDs[x]
        self._lastCleanup = now

    def registerSID(self, id, sid):
        self._idleIDs[id].sid = sid

    def createGame(self, playerID, partnerID):
        if(playerID in self._idleIDs and partnerID in self._idleIDs):
            if self._idleIDs[playerID].sid == None or self._idleIDs[partnerID].sid == None:
                return False
            game = {"white": playerID, "black": partnerID, "whitesTurn": True}
            self._idleIDs[playerID].game = game
            self._idleIDs[playerID].partner = self._idleIDs[partnerID]
            self._idleIDs[partnerID].game = game
            self._idleIDs[partnerID].partner = self._idleIDs[playerID]
            self.sendMessage(
                self._idleIDs[playerID].sid, "startGame", {"moveFirst": True, "partnerID": partnerID})
            self.sendMessage(
                self._idleIDs[partnerID].sid, "startGame", {"moveFirst": False, "partnerID": playerID})
            return True
        else:
            return False

    def sendMessage(self, sid, msg, data=None):
        if data:
            self._socket.emit(msg, data, room=sid)
        else:
            self._socket.emit(msg, room=sid)

    def makeMove(self, id, i, j):
        # TODO add move validation on server side
        if id in self._idleIDs and self._idleIDs[id].game != None:
            game = self._idleIDs[id].game
        else:
            return False
        if game["whitesTurn"] != (game["white"] == id):
            return False
        receiver = self._idleIDs[id].partner.sid
        game["whitesTurn"] = not game["whitesTurn"]
        self._idleIDs[id].dt = datetime.datetime.now()
        self.sendMessage(receiver, "move", {"from": i, "to": j})
