from sqlalchemy import *
from flask_sqlalchemy import SQLAlchemy
import os
# TODO CREATE PLAYER INFO IN THE DB
# LOCAL
database_path = os.environ.get('DATABASE_URL')
SQLALCHEMY_TRACK_MODIFICATIONS = False
db = SQLAlchemy()


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


def db_drop_and_create_all():
    db.drop_all()
    db.create_all()


def create_db():
    db.create_all()


class Player(db.Model):
    __tablename__ = 'player'
    id = Column(Integer, primary_key=True)
    player_username = Column(String)
    player_username_uid = Column(String)
    kills = Column(Integer)
    killpermin = Column(Integer)
    accurecy = Column(Integer) # percentage
    RPM = Column(Integer) # A number represents chances that this player is
    # a cheater
    def __init__(self, player_username, kills):
        self.player_username = player_username
        self.kills = kills

        # TODO

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'player': self.player_username_uid,
            'release_date': self.kills,
        }

