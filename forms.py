from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, DateField, validators, IntegerField, SubmitField
from wtforms.validators import NumberRange, DataRequired, Optional, InputRequired
import persons
import matches


class LoginForm(FlaskForm):
    username = StringField("Username")
    password = PasswordField("Password")
    submit = SubmitField("Submit")


class RegistrationForm(FlaskForm):
    username = StringField("Username", [validators.Length(
        min=4, max=16, message="Username must be between 4 and 16 characters")])
    password = PasswordField("Password", [DataRequired(), validators.Length(
        min=5, message="Password must be at least 5 characters"),
        validators.EqualTo("confirm", message="Passwords must match")])
    confirm = PasswordField("Confirm Password")
    submit = SubmitField("Submit")


class SearchForm(FlaskForm):
    search = StringField("Search", [validators.Length(
        max=30, message="Search term must be less than 30 characters")])
    submit = SubmitField("Submit")


class FighterForm(FlaskForm):
    firstname = StringField("First Name", validators=[DataRequired()])
    lastname = StringField("Last Name", validators=[DataRequired()])
    nickname = StringField("Nickname")
    born = DateField("Born", validators=[DataRequired()], format="%Y-%m-%d")
    feet = IntegerField("Feet", validators=[
                        DataRequired(), NumberRange(min=4, max=7)])
    inches = IntegerField("Inches", validators=[
                          Optional(), NumberRange(min=0, max=11)])
    weight = IntegerField("Weight (lbs)", validators=[
                          DataRequired(), NumberRange(min=100, max=500)])
    country = SelectField("Country", coerce=int)


class FightForm(FlaskForm):
    fighter1 = SelectField("Fighter 1", coerce=int)
    fighter2 = SelectField("Fighter 2", coerce=int)
    referee = SelectField("Referee", coerce=int)
    rounds = IntegerField("Rounds", validators=[
                          DataRequired(), NumberRange(min=1, max=5)])
    ending_round = IntegerField("Ending Round", validators=[
                                DataRequired(), NumberRange(min=1, max=5)])
    minutes = IntegerField("Minutes", validators=[
                           InputRequired(), NumberRange(min=0, max=5)])
    seconds = IntegerField("Seconds", validators=[
                           InputRequired(), NumberRange(min=0, max=59)])
    winner = SelectField("Winner", coerce=int)
    winning_method = StringField("Winning Method", validators=[DataRequired()])
    date = DateField("Date", validators=[DataRequired()], format="%Y-%m-%d")
    event = SelectField("Event", coerce=int)
    fight_order = IntegerField("Fight Order", validators=[Optional()])
    weight_class = SelectField("Weight class", coerce=int, validators=[
                               DataRequired(), NumberRange(min=100, max=500)])
    submit = SubmitField("Submit")


class OfficialsForm(FlaskForm):
    firstname = StringField("First Name", validators=[
                            DataRequired(), validators.Length(min=2, max=30)])
    lastname = StringField("Last Name", validators=[
                           DataRequired(), validators.Length(min=2, max=30)])
    submit = SubmitField("Submit")


class EventForm(FlaskForm):
    name = StringField("Name", validators=[
                       DataRequired(), validators.Length(min=2, max=50)])
    date = DateField("Date", validators=[DataRequired()], format="%Y-%m-%d")
    location = StringField("Location", validators=[
                           DataRequired(), validators.Length(min=2, max=50)])
    promotion = StringField("Promotion", validators=[
                            DataRequired(), validators.Length(min=2, max=30)])
    submit = SubmitField("Submit")


class ScoreForm(FlaskForm):
    score_f1 = IntegerField(
        "R1", validators=[Optional(), NumberRange(min=21, max=50)])
    score_f2 = IntegerField(
        "R2", validators=[Optional(), NumberRange(min=21, max=50)])
    comment = StringField("Comment", validators=[
                          Optional(), validators.Length(max=280)])
    submit = SubmitField("Submit")


class DateForm(FlaskForm):
    start_date = DateField("Date", validators=[Optional()], format="%Y-%m-%d")
    end_date = DateField("Date", validators=[Optional()], format="%Y-%m-%d")
    submit = SubmitField("Submit")


def setup_form_choices(form):
    form.fighter1.choices = [(fighter.id, fighter.lastname + ", " + fighter.firstname)
                             for fighter in persons.get_fighters()]
    form.fighter2.choices = [(fighter.id, fighter.lastname + ", " + fighter.firstname)
                             for fighter in persons.get_fighters()]
    form.winner.choices = [(-1, "Draw")] + [(fighter.id, fighter.lastname +
                                             ", " + fighter.firstname)
                                            for fighter in persons.get_fighters()]
    form.referee.choices = [(referee.id, referee.lastname + ", " + referee.firstname)
                            for referee in persons.get_referees()]
    form.event.choices = [(-1, "N/A")] + [(event.id, event.name)
                                          for event in matches.get_events("all")]
    form.weight_class.choices = persons.get_weight_classes()
