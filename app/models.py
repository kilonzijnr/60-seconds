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
    downvotes = db.relationship('Downvotes', backref = 'user' lazy = 'dynamic') 
    