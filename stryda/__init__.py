from flask_admin import Admin, expose, BaseView
from flask_admin.contrib.sqla import ModelView
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import flask_login as login
from flask_login import LoginManager
from os import path
from flask_basicauth import BasicAuth


db = SQLAlchemy()
DB_NAME = "stryda3.db"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "astral_codex"
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['FLASK_ADMIN_SWATCH'] = 'slate'

    db.init_app(app)

    from .models import User
    login_manager = LoginManager()
    login_manager.login_view = 'login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    create_db(app)
    return app


def create_db(app):
    if not path.exists('stryda/' + DB_NAME):
        db.create_all(app=app)
        print("sucess")


create_app()
