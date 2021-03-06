from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DateField, IntegerField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from app.models import User

class LoginForm(FlaskForm):
    username = StringField ('Username', validators=[DataRequired()])
    password = PasswordField ('Password', validators=[DataRequired()])
    remember_me = BooleanField ('Remember me')
    submit = SubmitField ('Sign in')


class RegistrationForm(FlaskForm):
    username = StringField ('Username', validators=[DataRequired()])
    email = StringField('Email', validators = [DataRequired(), Email()])
    password = PasswordField ('Password', validators=[DataRequired()])
    password2 = PasswordField(
            'Repeat Password', validators = [DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username = username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email = email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class EditProfileForm(FlaskForm):
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
    timestamp = DateField('Date', validators = [DataRequired()])
    category = StringField('Category', validators = [DataRequired(), Length(min =1, max = 140)])
    body = IntegerField('Sum of money', validators = [DataRequired()])
    submit = SubmitField('Submit')
