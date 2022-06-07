"""App module __init__"""

from flask import Flask
from flask_migrate import Migrate

from app.endpoints.todo import API_BP
from config import Config
from app import models
from app.models.db_init import DATABASE
from app.commands import CMD
from app import endpoints


MIGRATE = Migrate()


def create_app():
    """Function for creating app"""
    app = Flask(__name__)
    app.config.from_object(Config)
    DATABASE.init_app(app)
    app.register_blueprint(CMD, cli_group=None)
    app.register_blueprint(API_BP, url_prefix='/api')
    MIGRATE.init_app(app, DATABASE)
    return app
