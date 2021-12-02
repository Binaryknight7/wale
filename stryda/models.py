from . import db
from flask_login import UserMixin
import datetime

date = datetime.datetime.strftime(datetime.datetime.now(), '%B %d, %Y')


class User(db.Model, UserMixin):
    id = db.Column(db.Integer,
                   primary_key=True)
    email = db.Column(db.String(120),
                      nullable=False,
                      unique=False)
    password = db.Column(db.String(40),
                         unique=True,
                         nullable=False)

    date = db.Column(db.String(40),
                     unique=True,
                     nullable=False,
                     default=date)


class Admin_User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120))
    password = db.Column(db.String(64))
