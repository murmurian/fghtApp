from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, DateField, validators


class RegistrationForm(FlaskForm):
    username = StringField('Username', [validators.Length(min=4, max=16, message='Username must be between 4 and 16 characters')])
    password = PasswordField('Password', [validators.DataRequired(), validators.Length(
        min=5, message='Password must be at least 5 characters'), validators.EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Confirm Password')


class SearchForm(FlaskForm):
    q = StringField('Search', [validators.Length(max=30, message='Search term must be less than 30 characters')])


class FighterForm(FlaskForm):
    firstname = StringField('First Name', validators=[validators.DataRequired()])
    lastname = StringField('Last Name', validators=[validators.DataRequired()])
    nickname = StringField('Nickname')
    born = DateField('Born', format='%Y-%m-%d')
    height = StringField('Height')
    weight = StringField('Weight')
    country = SelectField('Country', coerce=int)

