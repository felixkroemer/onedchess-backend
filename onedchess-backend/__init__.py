from flask import Flask
from dotenv import load_dotenv
from .extensions import game


def create_app(config_file):
    app = Flask(__name__)

    load_dotenv('.env')
    app.config.from_pyfile('settings.py')

    game.init(app)

    from . import views
    app.register_blueprint(views.bp)

    return app
