from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DateTimeField, IntegerField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from app.models import User


class EditProfileForm(FlaskForm):
    """the form allows users to change their username and other data"""
    username = StringField('Username', validators = [DataRequired()])
    submit = SubmitField('Submit')

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm,self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self,username):
        if username.data != self.original_username:
            user = User.query.filter_by(username = self.username.data).first()
            if user is not None:
                raise ValidationError('Please use a different username')


class AddExpenseForm(FlaskForm):
    """the form allows users to change money spending"""
    timestamp = DateTimeField('Date', validators = [DataRequired()])
    category = StringField('Category', validators = [DataRequired(), Length(min =1, max = 140)])
    body = IntegerField('Sum of money', validators = [DataRequired()])
    submit = SubmitField('Submit')

