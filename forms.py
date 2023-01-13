from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, DateField, validators, IntegerField, SubmitField
from wtforms.validators import NumberRange, ValidationError


class RegistrationForm(FlaskForm):
    username = StringField("Username", [validators.Length(min=4, max=16, message="Username must be between 4 and 16 characters")])
    password = PasswordField("Password", [validators.DataRequired(), validators.Length(
        min=5, message="Password must be at least 5 characters"), validators.EqualTo("confirm", message="Passwords must match")])
    confirm = PasswordField("Confirm Password")
    submit = SubmitField("Submit")


class SearchForm(FlaskForm):
    q = StringField("Search", [validators.Length(max=30, message="Search term must be less than 30 characters")])
    submit = SubmitField("Submit")


class FighterForm(FlaskForm):
    firstname = StringField("First Name", validators=[validators.DataRequired()])
    lastname = StringField("Last Name", validators=[validators.DataRequired()])
    nickname = StringField("Nickname")
    born = DateField("Born", format="%Y-%m-%d")
    height = StringField("Height")
    weight = StringField("Weight")
    country = SelectField("Country", coerce=int)
    submit = SubmitField("Submit")


class FightForm(FlaskForm):
    fighter1 = SelectField("Fighter 1", coerce=int)
    fighter2 = SelectField("Fighter 2", coerce=int)
    referee = SelectField("Referee", coerce=int)
    rounds = IntegerField("Rounds", validators=[validators.DataRequired(), NumberRange(min=1, max=5)])
    ending_round = IntegerField("Ending Round", validators=[validators.DataRequired(), validators.NumberRange(min=1, max=5)])
    minutes = IntegerField("Minutes", validators=[validators.Optional(), validators.NumberRange(min=0, max=5)])
    seconds = IntegerField("Seconds", validators=[validators.Optional(), validators.NumberRange(min=0, max=59)])
    winner = SelectField("Winner", coerce=int)
    winning_method = StringField("Winning Method")
    date = DateField("Date", validators=[validators.DataRequired()], format="%Y-%m-%d")
    event = SelectField("Event", coerce=int)
    fight_order = IntegerField("Fight Order")
    weight_class = SelectField("Weight class", coerce=int)
    submit = SubmitField("Submit")
    
    def validate_fighter1(self, fighter1):
        if self.fighter1.data == self.fighter2.data:
            raise ValidationError("Fighter 1 and Fighter 2 must be different")
    
    def validate_winner(self, winner):
        if winner.data not in [self.fighter1.data, self.fighter2.data, "draw"]:
            raise ValidationError("Winner must be one of the fighters or a draw")

class OfficialsForm(FlaskForm):
    firstname = StringField("First Name", validators=[validators.DataRequired(), validators.Length(min=2, max=30)])
    lastname = StringField("Last Name", validators=[validators.DataRequired(), validators.Length(min=2, max=30)])
    submit = SubmitField("Submit")
    
