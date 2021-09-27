from typing import BinaryIO, DefaultDict
from sqlalchemy.sql.expression import false

from sqlalchemy.sql.functions import user
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

    @classmethod
    def get_pitches(cls, id):
        pitches =Pitch.query.order_by(pitch_id = id).desc().all()
        return pitches
   
    def save(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f'Pitch {self.description}'


class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    pitch_id = db.Column(db.Integer, db.ForeignKey('pitches.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    description = db.Column(db.Text)

    def __repr__(self):
        return f"Comment :id: {self.id} comment: {self.description}"


class Upvote(db.Model):
    __tablename__ = 'upvotes'

    id = db.Column(db.Integer, primary_key = True)
    upvote = db.Column(db.Integer, default=1)
    pitch_id = db.Column(db.Integer, db.ForeignKey('pitches.id'))
    user_id = db.Column(db.Interger,db.ForeignKey('users.id'))

    def save_upvotes(self):
        db.session.add(self)
        db.session.commit()

    def add_upvotes(cls,id):
        upvote_pitch = Upvote(user = current_user, pitch_id=id)
        upvote_pitch.save_upvotes()


    @classmethod
    def get_all_upvotes(cls, pitch_id):
        upvotes = Upvote.query.order_by('id').all()
        return upvotes

    def __repr__(self):
        return f'{self.user_id}:{self.pitch_id}'


class Downvote(db.Model):
    __table__name = 'downvotes'

    id = db.Column(db.Integer, primaary_key = True)
    downvote = db.Column(db.Integer, default = 1)
    pitch_id = db.Column(db.Integer, db.ForeignKey('pitches.id'))
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))

    def save_downvotes(self):
        db.session.add(self)
        db.session.commit()

    def add_downvotes(cls,id):
        downvote_pitch = Downvote(user = current_user, pitch_id=id)
        downvote_pitch.save_downvotes()


    @classmethod
    def get_downvotes(cls,id):
        downvote = Downvote.query.filter_by(pitch_id=id).all()
        return downvote

    @classmethod
    def get_all_downvotes(cls,pitch_id):
        downvote = Downvote.query.order_by('id').all()
        return downvote

    def __repr__(self):
        return f'{self.user_id}:{self.pitch_id}'




        



    





