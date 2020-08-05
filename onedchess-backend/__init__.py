from flask import Flask
from dotenv import load_dotenv
from .extensions import game
from flask_cors import CORS


def create_app(config_file):
    app = Flask(__name__)

    load_dotenv('.env')
    app.config.from_pyfile('settings.py')

    origins = app.config.get('CORS_ORIGIN_WHITELIST', '*')
    CORS(app, supports_credentials=True, origins=origins)

    game.init(app)

    from . import views
    app.register_blueprint(views.bp)

    return app
