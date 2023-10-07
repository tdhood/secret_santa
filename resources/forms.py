from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Length, Optional

class LoginForm(FlaskForm):
    """Login Form"""

    username = StringField('Username', validators=[DataRequired()])
    password = StringField('Password', validators=[DataRequired()])


class UserSignUpForm(FlaskForm):
    """Form for signing up"""

    username = StringField('Username', validators=[DataRequired()])
    password = StringField('Password', validators=[DataRequired()])
    first_name = StringField('First Name', validators=[DataRequired()])


class UserEditForm(FlaskForm):
    """Form for editing user"""

    username = StringField('Username', validators=[DataRequired()])
    password = StringField('Password', validators=[DataRequired()])
    first_name = StringField('First Name', validators=[DataRequired()])
    wish_list = TextAreaField('Wish List', validators=[DataRequired()])
    helpful_notes = TextAreaField('Helpful Notes', validators=[Optional()])

class CSRFProtectForm(FlaskForm):
    """Form just for CSRF Protection"""