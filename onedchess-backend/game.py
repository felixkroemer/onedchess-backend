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

    def getIDs(self):
        return self._idleIDs.keys()

    def cleanIDs(self):
        now = datetime.datetime.now()
        for x in self._idleIDs.copy():
            diff = now - self._idleIDs[x].dt
            if(diff.days > 0 or diff.seconds > 1200):
                del self._idleIDs[x]
        self._lastCleanup = now

    def registerSID(self, id, sid):
        self._idleIDs[id].sid = sid
        game = self._idleIDs[id].game
        if game:
            player = self._idleIDs[id]
            moveNext = game["whitesTurn"] == (game["white"] == id)
            partnerID = game["black"] if game["white"] == id else game["white"]
            self.sendMessage(
                player.sid, "startGame", {"moveNext": moveNext, "field": game["field"],
                                          "partnerID": partnerID, "whitesTurn": game["whitesTurn"]})

    def createGame(self, playerID, partnerID):
        if(playerID in self._idleIDs and partnerID in self._idleIDs):
            if self._idleIDs[playerID].sid == None or self._idleIDs[partnerID].sid == None:
                return False
            field = [
                (False, "ROOK"),
                (False, "KNIGHT"),
                (False, "KING"),
                (False, "KNIGHT"),
                (False, "ROOK"),
                None,
                None,
                (True, "ROOK"),
                (True, "KNIGHT"),
                (True, "KING"),
                (True, "KNIGHT"),
                (True, "ROOK"),
            ]
            game = {"white": playerID, "black": partnerID,
                    "whitesTurn": True, "field": field}
            self._idleIDs[playerID].game = game
            self._idleIDs[playerID].partner = self._idleIDs[partnerID]
            self._idleIDs[partnerID].game = game
            self._idleIDs[partnerID].partner = self._idleIDs[playerID]
            self.sendMessage(
                self._idleIDs[playerID].sid, "startGame", {"moveNext": True, "partnerID": partnerID})
            self.sendMessage(
                self._idleIDs[partnerID].sid, "startGame", {"moveNext": False, "partnerID": playerID})
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
            field = game["field"]
            switch = False
            if field[j] and field[i][1] == "ROOK" and field[j][1] == "KING" or field[i][1] == "KING" and field[j][1] == "ROOK":
                temp = field[j]
                switch = True
            game["field"][j] = game["field"][i]
            game["field"][i] = temp if switch else None
        else:
            return False
        if game["whitesTurn"] != (game["white"] == id):
            return False
        receiver = self._idleIDs[id].partner.sid
        game["whitesTurn"] = not game["whitesTurn"]
        self._idleIDs[id].dt = datetime.datetime.now()
        self.sendMessage(receiver, "move", {"from": i, "to": j})

    def quitGame(self, id):
        receiver = self._idleIDs[id].partner.sid
        self._idleIDs[id].partner.game = None
        self._idleIDs[id].partner.partner = None
        self._idleIDs[id].game = None
        self._idleIDs[id].partner = None
        self.sendMessage(receiver, "quitGame")
