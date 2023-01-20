from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, DateField, validators, IntegerField, SubmitField
from wtforms.validators import NumberRange, ValidationError, DataRequired, Optional
from wtforms.widgets import TextArea


class LoginForm(FlaskForm):
    username = StringField("Username")
    password = PasswordField("Password")
    submit = SubmitField("Submit")


class RegistrationForm(FlaskForm):
    username = StringField("Username", [validators.Length(min=4, max=16, message="Username must be between 4 and 16 characters")])
    password = PasswordField("Password", [DataRequired(), validators.Length(
        min=5, message="Password must be at least 5 characters"), validators.EqualTo("confirm", message="Passwords must match")])
    confirm = PasswordField("Confirm Password")
    submit = SubmitField("Submit")


class SearchForm(FlaskForm):
    q = StringField("Search", [validators.Length(max=30, message="Search term must be less than 30 characters")])
    submit = SubmitField("Submit")


class FighterForm(FlaskForm):
    firstname = StringField("First Name", validators=[DataRequired()])
    lastname = StringField("Last Name", validators=[DataRequired()])
    nickname = StringField("Nickname")
    born = DateField("Born", validators=[DataRequired()], format="%Y-%m-%d")
    feet = IntegerField("Feet", validators=[DataRequired(), NumberRange(min=4, max=7)])
    inches = IntegerField("Inches", validators=[validators.Optional(), NumberRange(min=0, max=11)])
    weight = IntegerField("Weight (lbs)", validators=[DataRequired(), NumberRange(min=100, max=500)])
    country = SelectField("Country", coerce=int)


class FightForm(FlaskForm):
    fighter1 = SelectField("Fighter 1", coerce=int)
    fighter2 = SelectField("Fighter 2", coerce=int)
    referee = SelectField("Referee", coerce=int)
    rounds = IntegerField("Rounds", validators=[DataRequired(), NumberRange(min=1, max=5)])
    ending_round = IntegerField("Ending Round", validators=[DataRequired(), NumberRange(min=1, max=5)])
    minutes = IntegerField("Minutes", validators=[Optional(), NumberRange(min=0, max=5)])
    seconds = IntegerField("Seconds", validators=[Optional(), NumberRange(min=0, max=59)])
    winner = SelectField("Winner", coerce=int)
    winning_method = StringField("Winning Method", validators=[DataRequired()])
    date = DateField("Date", validators=[DataRequired()], format="%Y-%m-%d")
    event = SelectField("Event", coerce=int)
    fight_order = IntegerField("Fight Order")
    weight_class = SelectField("Weight class", coerce=int, validators=[DataRequired(), NumberRange(min=100, max=500)])
    submit = SubmitField("Submit")
    
    def validate_fighter1(self, fighter1):
        if self.fighter1.data == self.fighter2.data:
            raise ValidationError("Fighter 1 and Fighter 2 must be different")
    
    def validate_winner(self, winner):
        if winner.data not in [self.fighter1.data, self.fighter2.data, -1]:
            raise ValidationError("Winner must be one of the fighters or a draw")


class OfficialsForm(FlaskForm):
    firstname = StringField("First Name", validators=[DataRequired(), validators.Length(min=2, max=30)])
    lastname = StringField("Last Name", validators=[DataRequired(), validators.Length(min=2, max=30)])
    submit = SubmitField("Submit")


class EventForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), validators.Length(min=2, max=50)])
    date = DateField("Date", validators=[DataRequired()], format="%Y-%m-%d")
    location = StringField("Location", validators=[DataRequired(), validators.Length(min=2, max=50)])
    promotion = StringField("Promotion", validators=[DataRequired(), validators.Length(min=2, max=30)])
    submit = SubmitField("Submit")


class ScoreForm(FlaskForm):
    score_f1 = IntegerField("R1", validators=[Optional(), NumberRange(min=20, max=50)])
    score_f2 = IntegerField("R2", validators=[Optional(), NumberRange(min=20, max=50)])
    comment = StringField("Comment", validators=[Optional(), validators.Length(max=280)])
    submit = SubmitField("Submit")
