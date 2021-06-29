from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DateTimeField, IntegerField, FloatField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length, NumberRange, StopValidation
#from my_form import MyDataRequired
from app.models import User
import six

class MyDataRequired(object):
    """
    Checks the field's data is 'truthy' otherwise stops the validation chain.

    This validator checks that the ``data`` attribute on the field is a 'true'
    value (effectively, it does ``if field.data``.) Furthermore, if the data
    is a string type, a string containing only whitespace characters is
    considered false.

    If the data is empty, also removes prior errors (such as processing errors)
    from the field.

    **NOTE** this validator used to be called `Required` but the way it behaved
    (requiring coerced data, not input data) meant it functioned in a way
    which was not symmetric to the `Optional` validator and furthermore caused
    confusion with certain fields which coerced data to 'falsey' values like
    ``0``, ``Decimal(0)``, ``time(0)`` etc. Unless a very specific reason
    exists, we recommend using the :class:`InputRequired` instead.

    :param message:
        Error message to raise in case of a validation error.
    """
    field_flags = ('required', )

    def __init__(self, message=None):
        self.message = message

    def __call__(self, form, field):
        #field.data= float(field.data.replace(',','.'))
        if not field.data or isinstance(field.data, six.string_types) and not field.data.strip():
            if self.message is None:
                message = field.gettext('you cannot add empty field and you cannot use , . Use . instead.')
            else:
                message = self.message

            field.errors[:] = []
            raise StopValidation(message)
        if field.data <= 0 :
            if self.message is None:
                message = field.gettext('You cannot add zero or below zero expense.')
            else:
                message = self.message
            field.errors[:] = []
            raise StopValidation(message)
#        if not field.data or isinstance(field.data, string_types) and not field.data.strip():
#            if self.message is None:
#                message = field.gettext('This field is required.')
#            else:
#                message = self.message
#
#            field.errors[:] = []
#            raise StopValidation(message)

class Regexp(object):
    """
    Validates the field against a user provided regexp.

    :param regex:
        The regular expression string to use. Can also be a compiled regular
        expression pattern.
    :param flags:
        The regexp flags to use, for example re.IGNORECASE. Ignored if
        `regex` is not a string.
    :param message:
        Error message to raise in case of a validation error.
    """
    def __init__(self, regex, flags=0, message=None):
        if isinstance(regex, string_types):
            regex = re.compile(regex, flags)
        self.regex = regex
        self.message = message

    def __call__(self, form, field, message=None):
        match = self.regex.match(field.data or '')
        if not match:
            if message is None:
                if self.message is None:
                    message = field.gettext('Invalid input.')
                else:
                    message = self.message

            raise ValidationError(message)
        return match


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
    body = FloatField('Sum of money', validators = [MyDataRequired()])
    submit = SubmitField('Submit')


