from flask import Flask
from dotenv import load_dotenv
from flask_socketio import SocketIO
from flask_cors import CORS
from .extensions import game, socketio
import sys


def create_app(config_file):
    app = Flask(__name__)

    load_dotenv('.env')
    app.config.from_pyfile('settings.py')

    CORS(app, supports_credentials=True)

    socketio.init_app(app, cors_allowed_origins="*")
    game.init(app, socketio)

    from . import views
    app.register_blueprint(views.bp)

    return app
