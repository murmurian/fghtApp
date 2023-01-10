from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators


class RegistrationForm(FlaskForm):
    username = StringField('Username', [validators.Length(min=4, max=16, message='Username must be between 4 and 16 characters')])
    password = PasswordField('Password', [validators.DataRequired(), validators.Length(
        min=5, message='Password must be at least 5 characters'), validators.EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Confirm Password')


class SearchForm(FlaskForm):
    q = StringField('Search', [validators.Length(max=30, message='Search term must be less than 30 characters')])
