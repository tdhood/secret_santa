from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, EmailField, IntegerField
from wtforms.validators import DataRequired, Length, Optional, Email

class LoginForm(FlaskForm):
    """Login Form"""

    username = StringField('Username', validators=[DataRequired()])
    password = StringField('Password', validators=[DataRequired()])


class UserSignUpForm(FlaskForm):
    """Form for signing up"""
    class Meta:
        csrf = False

    username = StringField('Username', validators=[DataRequired()])
    password = StringField('Password', validators=[DataRequired()])
    first_name = StringField('First Name', validators=[DataRequired()])
    phone_number = StringField('Phone Number', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired(), Email()])


class UserEditForm(FlaskForm):
    """Form for editing user"""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    first_name = StringField('First Name', validators=[DataRequired()])
    wish_list = TextAreaField('Wish List', validators=[DataRequired()])
    helpful_notes = TextAreaField('Helpful Notes', validators=[Optional()])

class CSRFProtectForm(FlaskForm):
    """Form just for CSRF Protection"""