from .extensions import game
from .extensions import socketio
from flask_socketio import join_room
import time

from flask import Blueprint, session, jsonify, abort, request
from string import ascii_letters

bp = Blueprint('api', __name__, url_prefix='/api')


@bp.route('/getID')
def register():
    game.cleanIDs()
    if not ('id' in session and game.hasID(session['id'])):
        id = game.createID()
        if id:
            session["id"] = id
        else:
            abort(500)
    return jsonify({"id": session["id"]})


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


@socketio.on('registerSID')
def connect():
    join_room(request.sid)
    game.registerSID(session["id"], request.sid)


@socketio.on('makeMove')
def makeMove(data):
    game.makeMove(session["id"], data["from"], data["to"])
