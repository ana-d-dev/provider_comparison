"""
Flask-WTF form definitions for user authentication.

This module defines forms used for user registration and login.
It includes validation rules for usernames and passwords to ensure
basic security and input consistency.
"""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Length, Regexp


class RegistrationForm(FlaskForm):
    """
    Form used for creating a new user account.

    Validates:
    - Username: 3–10 characters, no spaces
    - Password: 8–23 characters, must include letters, numbers, and symbols
    """
    username = StringField(
        'Username',
        validators=[
            DataRequired(),
            Length(min=3, max=10),
            Regexp(
                r'^[^\s]{3,10}$',
                message="3–10 characters, no spaces allowed"
            )
        ]
    )

    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            Length(min=8, max=23),
            Regexp(
                r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[^A-Za-z0-9]).+$',
                message="Must include letters, numbers & a symbols"
            )
        ]
    )


class LoginForm(FlaskForm):
    """
    Form used for user login.

    Validates:
    - Username: required field
    - Password: required field
    """
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
