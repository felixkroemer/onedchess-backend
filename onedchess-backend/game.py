import datetime
import random
import string


class Game():

    def __init__(self):
        self._app = None
        self._socket = None
        self._idleIDs = {}
        self._games = {}
        self._partners = {}
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
                self._idleIDs[id] = [datetime.datetime.now(), None]
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
        for x in self._idleIDs.copy():
            diff = now - self._idleIDs[x][0]
            if(diff.days > 0 or diff.seconds > 1200):
                del self._idleIDs[x]
        self._lastCleanup = now

    def registerSID(self, id, sid):
        self._idleIDs[id][1] = sid

    def createGame(self, playerID, partnerID):
        if(playerID in self._idleIDs and partnerID in self._idleIDs):
            if(self._idleIDs[playerID][1] == None or self._idleIDs[partnerID][1] == None):
                return False
            self._games[playerID] = {"playerTurn": True, "partner": partnerID}
            self._games[playerID]["sids"] = (
                self._idleIDs[playerID][1], self._idleIDs[partnerID][1])
            self._idleIDs.pop(playerID)
            self._idleIDs.pop(partnerID)
            self._partners[partnerID] = playerID
            self.sendMessage(
                self._games[playerID]["sids"][0], "startGame", {"moveFirst": True})
            self.sendMessage(
                self._games[playerID]["sids"][1], "startGame", {"moveFirst": False})
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
        game = None
        if id in self._games:
            game = self._games[id]
            isPlayer = True
        if id in self._partners:
            game = self._games[self._partners[id]]
            isPlayer = False
        if not game:
            return
        if game["playerTurn"] != isPlayer:
            return
        receiver = game["sids"][1] if isPlayer else game["sids"][0]
        game["playerTurn"] = not game["playerTurn"]
        self.sendMessage(receiver, "move", {"from": i, "to": j})
