from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from app.models import User


class LoginForm(FlaskForm):
    """a form for logging in an existing user"""
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


def check_password2(password):
    password = str(password)
    l=len(password)
    c=0
    b=0
    print(password)
    for el in password:
        if el.isdigit():
            c+=1
            print(2)
        if el.istitle():
            b+=1
            print(1)
    if c == 0 or b == 0 or l<6:
        return False
    return True

class RegistrationForm(FlaskForm):
    """form for registering a new user"""
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(),Length(min=6,message='Password should be at least 6 characters long')])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(),
                                           EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        """the function of checking for a match of the username"""
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        """the function of checking for a match of the username"""
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


#    def check_password(password):
#        l = len(password)
#        c = 0
#        b = 0
#        for el in password:
#            if el.isdigit:
#    	        c+=1
#    	    if el.isupper:
#    	        b+=1
#    	if c == 0 or b == 0 or l<6:
#    	    return False
#    	return True
    	

#    def check_password2(password):
#        l=len(password)
#        c=0
#        d=0
#        for el in password:
#            if el.isdigit:
#                c+=1
#            if el.isupper:
#                b+=1
#        if c == 0 and b == 0 or l<6:
#            return False
#        return True
            
    def validate_password(self, password):
        """the function of checking for a match of the password"""
        #user = User.query.filter_by(password=password.data).first()
        if check_password2(str(password)) is False:
            print(233)
            raise ValidationError('Please choose correct password. Your password must contain 6 charecters of which one is a number and one is an uppercase letter.')


#def check_password2(password):
#        l=len(password)
#        c=0
#        d=0
#        for el in password:
#            if el.isdigit:
#                c+=1
#            if el.isupper:
#                b+=1
#        if c == 0 and b == 0 or l<6:
#            return False
#        return True

class ResetPasswordRequestForm(FlaskForm):
    """the form allows you to reset the password from an existing account"""
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')


class ResetPasswordForm(FlaskForm):
    """The form allows you to reset your password when logging in"""
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        ('Repeat Password'), validators=[DataRequired(),
                                           EqualTo('password')])
    submit = SubmitField('Request Password Reset')
