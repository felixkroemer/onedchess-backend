from .extensions import game
from .extensions import socketio
from flask_socketio import join_room
import time
import os
import psutil
from .settings import DEBUG_KEY

from flask import Blueprint, session, jsonify, abort, request
from string import ascii_letters

bp = Blueprint('api', __name__, url_prefix='/onedchess/api')


@bp.route('/getID')
def register():
    game.cleanIDs()
    if not ('id' in session and game.hasID(session['id'])):
        id = game.createID()
        if id:
            session["id"] = id
        else:
            abort(500)
    return {"id": session["id"]}


@bp.route('/setPartnerID', methods=['POST'])
def setPartnerID():
    if not ('id' in session and game.hasID(session['id'])):
        abort(500)
    if len(request.data) != 5 or not all(chr(x) in ascii_letters for x in request.data):
        abort(501)
    partnerID = request.data.decode().upper()
    if not game.hasID(partnerID):
        abort(502)
    if game.createGame(session["id"], partnerID):
        return ''
    else:
        abort(503)

@bp.route('/debug', methods=['POST'])
def debug():
    if(request.form["key"] != DEBUG_KEY):
        abort(401)
    else:
        ret = {}
        ret["ids"] = [x for x in game.getIDs()]
        process = psutil.Process(os.getpid())
        ret["memory usage"] = process.memory_info().rss
        return ret

@socketio.on('registerSID')
def connect():
    if "id" in session and game.hasID(session['id']):
        join_room(request.sid)
        game.registerSID(session["id"], request.sid)

@socketio.on('makeMove')
def makeMove(data):
    if "id" in session:
        game.makeMove(session["id"], data["from"], data["to"])
    else:
        abort(500)

@socketio.on('quitGame')
def quitGame():
    if "id" in session:
        game.quitGame(session["id"])
    else:
        abort(500)