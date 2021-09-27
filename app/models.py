from typing import BinaryIO
from app import email
from .import db
from sqlalchemy.sql import func
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, current_user

from .import login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primry_key =  True)
    username = db.Column(db.String(255))
    email = db.Column(db.string(255))
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())
    pass_secure = db.column(db.string(255))
    pitch = db.relationship('Pitch', backref='user', lazy='dynamic')
    comment = db.relationship('comment', backref='user', lazy='dynamic')
    upvotes = db.relationsip('upvote', backref = 'user', lazy ='dynamic')
    downvotes = db.relationship('Downvotes', backref = 'user', lazy = 'dynamic') 

    @property
    def password(self):
        raise AttributeError('You dont have access Priviledge for this action')

    @password.setter
    def password(self, password):
        self.pass_secure = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.pass_secure,password)

    def __repr__(self):
        return f'User'{self.username}

class Pitch(db.Model):

    __tablename__ = 'pitches'

    id = db.Column(db.Integer, primary_key = True)
    owner_id = db.column(db.Integer, db.ForeignKey('users.id'))
    description = db.column(db.String(), index = True)
    title = db.column(db.String())
    pitcher = db.column(db.String())
    category = db.relationship('comment', backref='pitch',lazy='dynamic') 
    upvotes = db.relationship('Upvote', backref = 'pitch', lazy = 'dynamic')
    downvotes = db.relationship('Downvote', backref = 'pitch', lazy = 'dynamic')





