"""App module __init__"""

from flask import Flask
from flask_migrate import Migrate
from flask_login import LoginManager

from app.endpoints.todo import api_bp
from config import Config
from app import models, endpoints
from app.models.db_init import DATABASE
from app.commands import cmd
from app.auth import AUTH
from app.models import User


MIGRATE = Migrate()


def create_app():
    """Function for creating app"""
    app = Flask(__name__)
    app.config.from_object(Config)
    DATABASE.init_app(app)
    app.register_blueprint(cmd, cli_group=None)
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(AUTH)
    MIGRATE.init_app(app, DATABASE)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login_post'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app
