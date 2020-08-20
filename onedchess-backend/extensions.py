from .game import Game
from flask_socketio import SocketIO

game = Game()
socketio = SocketIO(path="/onedchess/api/socketio/")
