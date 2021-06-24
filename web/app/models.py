from datetime import datetime
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login
from hashlib import md5
from time import time
import jwt
from flask import current_app
#from app import app

class User(UserMixin,db.Model):
    """generates avatar URLs for the user model"""
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), index = True, unique = True)
    email = db.Column(db.String(120), index = True, unique = True)
    password_hash = db.Column(db.String(128))
    expenses = db.relationship('Expense', backref = 'author', lazy = 'dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)

    #def expense(self):
        #return Expense.query.order_by(Expense.timestamp.desc())

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)


class Expense(db.Model):
    """generates finance for a specific user"""
    id = db.Column(db.Integer, primary_key = True)
    category = db.Column(db.String(64), index = True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Category {}, Expense {}>'.format(self.category,self.body)

@login.user_loader
def load_user(id):
    """function for uploading a user with an id"""
    return User.query.get(int(id))
