from .extensions import game

from flask import Blueprint, session, jsonify, abort, request

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
    print(request.data)
    return ''
