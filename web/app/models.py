from datetime import datetime
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login
from hashlib import md5
from time import time
import jwt
from flask import current_app

class User(UserMixin,db.Model):
    """ Class creates a User model inherited from base class of all models 

    id - a primary key automatically assigned by the database
    username - a field defined as string or VARCHAR
    email - a field defined as string or VARCHAR
    password hash - a field defined as string or VARCHAR
    expenses - establishes a relationship between user and his expenses (relationship one to many, defining on the side of one)

    """

    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), index = True, unique = True)
    email = db.Column(db.String(120), index = True, unique = True)
    password_hash = db.Column(db.String(128))
    expenses = db.relationship('Expense', backref = 'author', lazy = 'dynamic') #the first argument of db.relationship refences the side many, bacref defines the name of the field which will be added to the class objects 'many'

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)


    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'], algorithm='HS256')


    @staticmethod
    def verify_reset_password_token(app, token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)


class Expense(db.Model):
    """ Class creates an Expense model inherited from base class of all models 

    id - a primary key automatically assigned by the database
    category - a field defined as string or VARCHAR
    body - a field defined as string or VARCHAR
    timestamp - a field with the format DateTime
    user_id - a foreign key for user.id (it refences on the meaning id in the user. user is a name for the table of the class model)
    """
    id = db.Column(db.Integer, primary_key = True)
    category = db.Column(db.String(64), index = True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Category {}, Expense {}>'.format(self.category,self.body)

    def export_date(self):
        return str(self.timestamp.month)+'-'+str(self.timestamp.year)


@login.user_loader
def load_user(id):
    """ Function helping Flask-Login to upload the user """
    return User.query.get(int(id))
