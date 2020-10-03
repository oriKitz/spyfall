from spyfall import db, login_manager
from flask_login import UserMixin
import datetime


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    rooms = db.relationship('Room', secondary='room_user')

    def __repr__(self):
        return self.username


class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.String(20))
    admin = db.Column(db.Integer, db.ForeignKey('user.id'))
    users = db.relationship('User', secondary='room_user')
    game_status = db.Column(db.String(50))
    spy = db.Column(db.Integer, db.ForeignKey('user.id'))
    location = db.Column(db.String(200))


class RoomUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    last_connected = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
