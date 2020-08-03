from .extensions import game

from flask import Blueprint

bp = Blueprint('api', __name__, url_prefix='/api')


@bp.route('/register')
def register():
    return ""
