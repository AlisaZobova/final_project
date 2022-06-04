"""App module __init__"""

from flask import Flask
from flask_migrate import Migrate
from config import Config
from app import models
from app.models.db_init import DATABASE
from app.commands import cmd


MIGRATE = Migrate()


def create_app():
    """Function for creating app"""
    app = Flask(__name__)
    app.config.from_object(Config)
    DATABASE.init_app(app)
    app.register_blueprint(cmd, cli_group=None)
    MIGRATE.init_app(app, DATABASE)
    return app
