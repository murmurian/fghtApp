from app import app
from db import db
from flask import flash, redirect, render_template, request, session
from forms import FighterForm, OfficialsForm, RegistrationForm, SearchForm, FightForm, LoginForm
import users
import persons
import matches


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if session.get("user_id"):
        flash("You are already logged in!")
        return redirect("/")
    form = LoginForm()
    username = form.username.data
    password = form.password.data
    if request.method == "GET":
        return render_template("login.html", form=form, session=session)
    if users.login(username, password):
        flash("Welcome back, " + username + "!")
        return redirect("/")
    else:
        flash("No such username or password")
    return render_template("login.html", form=form, session=session)


@app.route("/logout")
def logout():
    if session.get("user_id"):
        del session["user_id"]
        flash("You have been logged out")
    return redirect("/")


@app.route("/admin")
def admin():
    user_id = session.get("user_id")
    if not user_id or not users.is_admin(user_id):
        flash("You are not authorized to view this page")
        return redirect("/")
    return render_template("admin.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if session.get("user_id"):
        flash("Please log out before registering a new account")
        return redirect("/")
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        if not users.register(username, password):
            flash("Username already registered")
            return render_template("/register.html", form=form)
        return redirect("/login")
    return render_template("register.html", form=form)


@app.route("/fighters", methods=["GET", "POST"])
def fighters_route():
    form = SearchForm()
    if request.method == "POST" and form.validate_on_submit() and form.q.data:
        query = form.q.data
        sql = "SELECT fighters.*, countries.name AS country_name, EXTRACT(YEAR FROM CURRENT_DATE) - EXTRACT(YEAR FROM born) AS age FROM fighters JOIN countries ON fighters.country = countries.id WHERE fighters.firstname like :query or fighters.lastname like :query or countries.name like :query"
        result = db.session.execute(sql, {"query": "%"+query+"%"})
    else:
        result = db.session.execute(
            "SELECT fighters.*, countries.name AS country_name, EXTRACT(YEAR FROM CURRENT_DATE) - EXTRACT(YEAR FROM born) AS age FROM fighters JOIN countries ON fighters.country = countries.id")
    fighters = result.fetchall()
    return render_template("fighters.html", count=len(fighters), fighters=fighters, form=form)


@app.route("/fighters/new", methods=["GET", "POST"])
def add_fighter():
    if not users.authorize():
        flash("You are not authorized to add fighters")
        return redirect("/fighters")
    form = FighterForm()
    form.country.choices = [(country.id, country.name) for country in matches.get_countries()]
    if request.method == "POST" and form.validate_on_submit():
        if persons.add_fighter(form):
            flash("Fighter added successfully")
            fighter_id = persons.get_fighter_id(form.firstname.data, form.lastname.data, form.born.data)
            fighter = persons.get_fighter(fighter_id)
            return render_template("add_fighter.html", form=form, is_new=False, fighter=fighter)
        else:
            flash("Fighter already in database")
    return render_template("add_fighter.html", form=form, is_new=True)


@app.route("/fighters/edit/<int:fighter_id>", methods=["GET", "POST"])
def edit_fighter(fighter_id):
    if not users.authorize():
        flash("You are not authorized to edit fighters")
        return redirect("/fighters/" + str(fighter_id))
    fighter=persons.get_fighter(fighter_id)
    form=FighterForm()
    form.country.choices=[(country.id, country.name) for country in matches.get_countries()]
    if request.method == "POST" and form.validate_on_submit():
        persons.edit_fighter(form, fighter_id)
        flash("Fighter info updated")
    return render_template("add_fighter.html", form=form, is_new=False, fighter=fighter)


@app.route("/fighters/delete/<int:fighter_id>")
def delete_fighter(fighter_id):
    if not users.authorize():
        flash("You are not authorized to delete fighters")
        return redirect("/fighters/edit/" + str(fighter_id))
    persons.delete_fighter(fighter_id)
    flash("Fighter deleted")
    return redirect("/fighters")


@app.route("/fighters/<int:fighter_id>")
def fighter_profile(fighter_id):
    fighter = persons.get_fighter(fighter_id)
    fights = matches.fights_by_id(fighter_id)
    is_admin = users.is_admin(session.get("user_id"))
    if fighter:
        return render_template("fighter.html", fighter=fighter, fights=fights, is_admin=is_admin)
    else:
        flash("Fighter not found")
        return redirect("/fighters")


@app.route("/fights")
def fights_route():
    fights = matches.get_fightlist(None)
    return render_template("fights.html", count=len(fights), fights=fights)


@app.route("/fights/new", methods=["GET", "POST"])
def add_fight():
    if not users.authorize():
        flash("You are not authorized to add fights")
        return redirect("/fights")
    form = FightForm()
    form.fighter1.choices= [(fighter.id, fighter.lastname + ", " + fighter.firstname) for fighter in persons.get_fighters()]
    form.fighter2.choices= [(fighter.id, fighter.lastname + ", " + fighter.firstname) for fighter in persons.get_fighters()]
    form.winner.choices = [(-1, "Draw")] + [(fighter.id, fighter.lastname + ", " + fighter.firstname) for fighter in persons.get_fighters()]
    form.referee.choices= [(referee.id, referee.lastname + ", " + referee.firstname) for referee in persons.get_referees()]
    form.event.choices = [(-1, "N/A")] + [(event.id, event.name) for event in matches.get_events()]
    form.weight_class.choices = persons.get_weight_classes()
    if request.method == "POST" and form.validate_on_submit():
        if matches.add_fight(form):
            flash("Fight added successfully")
        else:
            flash("Fight already exists")
    return render_template("add_fight.html", form=form, is_new=True)


@app.route("/fights/edit/<int:fight_id>", methods=["GET", "POST"])
def edit_fight(fight_id):
    if not users.authorize():
        flash("You are not authorized to edit fights")
        return redirect("/fights/" + str(fight_id))
    fight = matches.get_fight(fight_id)
    form = FightForm()
    form.fighter1.choices= [(fighter.id, fighter.lastname + ", " + fighter.firstname) for fighter in persons.get_fighters()]
    form.fighter2.choices= [(fighter.id, fighter.lastname + ", " + fighter.firstname) for fighter in persons.get_fighters()]
    form.winner.choices = [(-1, "Draw")] + [(fighter.id, fighter.lastname + ", " + fighter.firstname) for fighter in persons.get_fighters()]
    form.referee.choices= [(referee.id, referee.lastname + ", " + referee.firstname) for referee in persons.get_referees()]
    form.event.choices = [(-1, "N/A")] + [(event.id, event.name) for event in matches.get_events()]
    form.weight_class.choices = persons.get_weight_classes()
    final_round = matches.final_round(fight.ending_time.strftime("%M:%S"))
    ending_time = matches.ending_time(final_round, fight.ending_time.strftime("%M:%S"))
    minutes = ending_time.strftime("%M")
    seconds = ending_time.strftime("%S")
    if request.method == "POST" and form.validate_on_submit():
        matches.edit_fight(form, fight_id)
        flash("Fight info updated")
        return redirect("/fights/edit/" + str(fight_id) )
    return render_template("add_fight.html", form=form, is_new=False, fight=fight, final_round=final_round, minutes=minutes, seconds=seconds)


@app.route("/fights/delete/<int:fight_id>")
def delete_fight(fight_id):
    if not users.authorize():
        flash("You are not authorized to delete fights")
        return redirect("/fights/edit/" + str(fight_id))
    matches.delete_fight(fight_id)
    flash("Fight deleted")
    return redirect("/fights")


@app.route("/fights/<int:fight_id>")
def fight_detail(fight_id):
    fight = matches.get_fight(fight_id)
    is_admin = users.is_admin(session.get("user_id"))
    if fight:
        final_round = matches.final_round(fight.ending_time.strftime("%M:%S"))
        ending_time = matches.ending_time(final_round, fight.ending_time.strftime("%M:%S"))
        return render_template("fight.html", fight =fight, is_admin=is_admin, final_round=final_round, ending_time=ending_time)
    else:
        flash("Fight not found")
        return redirect("/fights")


@app.route("/referees/new", methods=["GET", "POST"])
def add_referee():
    if not users.authorize():
        flash("You are not authorized to add referees")
        return redirect("/referees")
    form = OfficialsForm()
    if request.method == "POST" and form.validate_on_submit():
        if persons.add_referee(form):
            flash("Referee added successfully")
        else:
            flash("Referee already exists")
    return render_template("add_official.html", form =form)


@app.route("/referees")
def referees_route():
    referees = persons.get_referees()
    return render_template("referees.html", count=len(referees), referees=referees)


@app.route("/referees/<int:referee_id>")
def referee_profile(referee_id):
    referee = persons.get_referee(referee_id)
    fights = matches.fights_by_referee(referee_id)
    if referee:
        return render_template("referee.html", referee=referee, fights=fights)
    else:
        flash("Referee not found")
        return redirect("/referees")


@app.route("/events", methods=["GET", "POST"])
def events_route():
    events = matches.get_events()
    return render_template("events.html", count=len(events), events=events)


@app.route("/events/<int:event_id>")
def event_detail(event_id):
    event = matches.get_event(event_id)
    fights = matches.get_fightlist(event_id)
    final_rounds = [matches.final_round(fight.ending_time.strftime("%H:%M:%S")) for fight in fights]
    ending_times = [matches.ending_time(final_round, fight.ending_time.strftime("%H:%M:%S")) for final_round, fight in zip(final_rounds, fights)]
    if event:
        return render_template("event.html", event =event, fights=fights, final_rounds=final_rounds, ending_times=ending_times)
    else:
        flash("Event not found")
        return redirect("/events")
