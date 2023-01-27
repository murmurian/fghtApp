from flask import flash, redirect, render_template, request, session
from app import app
from db import db
from forms import (
    DateForm,
    EventForm,
    FighterForm,
    OfficialsForm,
    RegistrationForm,
    SearchForm,
    FightForm,
    LoginForm,
    ScoreForm,
)
import users
import persons
import matches


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login/", methods=["GET", "POST"])
def login():
    if session.get("user_id"):
        flash("You are already logged in!")
        return redirect("/")
    form = LoginForm()
    username = form.username.data
    password = form.password.data
    if request.method == "POST":
        if users.login(username, password):
            flash("Welcome back, " + username + "!")
            return redirect("/")
        else:
            flash("No such username or password")
    return render_template("login.html", form=form, session=session)


@app.route("/logout/")
def logout():
    if session.get("user_id"):
        del session["user_id"]
        flash("You have been logged out")
    return redirect("/")


@app.route("/admin/")
def admin():
    user_id = session.get("user_id")
    if not user_id or not users.is_admin(user_id):
        flash("You are not authorized to view this page")
        return redirect("/")
    return render_template("admin.html")


@app.route("/register/", methods=["GET", "POST"])
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
        flash("Registration successful")
        return redirect("/login")
    return render_template("register.html", form=form)


@app.route("/fighters/", methods=["GET", "POST"])
def fighters_route():
    form = SearchForm()
    if request.method == "POST" and form.validate_on_submit():
        fighters = persons.search_fighters(form)
    else:
        fighters = persons.get_random_fighters()
    return render_template(
        "fighters.html",
        count=len(fighters),
        fighters=fighters,
        form=form,
    )


@app.route("/fighters/new", methods=["GET", "POST"])
def add_fighter():
    if not users.authorize():
        flash("You are not authorized to add fighters")
        return redirect("/fighters")
    form = FighterForm()
    form.country.choices = [
        (country.id, country.name) for country in matches.get_countries()
    ]
    if request.method == "POST" and form.validate_on_submit():
        if persons.add_fighter(form):
            flash("Fighter added successfully")
            fighter_id = persons.get_fighter_id(
                form.firstname.data, form.lastname.data, form.born.data
            )
            fighter = persons.get_fighter(fighter_id)
            return render_template("add_fighter.html", form=form, fighter=fighter)
        else:
            flash("Fighter already in database")
    return render_template("add_fighter.html", form=form, is_new=True)


@app.route("/fighters/edit/<int:fighter_id>", methods=["GET", "POST"])
def edit_fighter(fighter_id):
    if not users.authorize():
        flash("You are not authorized to edit fighters")
        return redirect("/fighters/" + str(fighter_id))
    fighter = persons.get_fighter(fighter_id)
    if not fighter:
        flash("Fighter not found")
        return redirect("/fighters")
    form = FighterForm()
    form.country.choices = [
        (country.id, country.name) for country in matches.get_countries()
    ]
    if request.method == "POST" and form.validate_on_submit():
        persons.edit_fighter(form, fighter_id)
        flash("Fighter info updated")
    fighter = persons.get_fighter(fighter_id)
    return render_template("add_fighter.html", form=form, fighter=fighter)


@app.route("/fighters/delete/<int:fighter_id>", methods=["POST"])
def delete_fighter(fighter_id):
    if not users.authorize():
        flash("You are not authorized to delete fighters")
        return redirect("/fighters/edit/" + str(fighter_id))
    if not persons.get_fighter(fighter_id):
        flash("Fighter not found")
        return redirect("/fighters")
    persons.delete_fighter(fighter_id)
    flash("Fighter deleted")
    return redirect("/fighters")


@app.route("/fighters/<int:fighter_id>")
def fighter_profile(fighter_id):
    fighter = persons.get_fighter(fighter_id)
    fights = matches.fights_by_id("fighter", fighter_id)
    if fighter:
        return render_template(
            "fighter.html", fighter=fighter, fights=fights, is_admin=users.authorize()
        )
    else:
        flash("Fighter not found")
        return redirect("/fighters")


@app.route("/fights/", methods=["GET", "POST"])
def fights_route():
    form = DateForm()
    if request.method == "POST" and form.validate_on_submit():
        fights = matches.get_fights_by_dates(form)
    else:
        fights = matches.get_fightlist(None)
    return render_template("fights.html", count=len(fights), fights=fights, form=form)


@app.route("/fights/new", methods=["GET", "POST"])
def add_fight():
    if not users.authorize():
        flash("You are not authorized to add fights")
        return redirect("/fights")
    form = FightForm()
    form.fighter1.choices = [
        (fighter.id, fighter.lastname + ", " + fighter.firstname)
        for fighter in persons.get_fighters()
    ]
    form.fighter2.choices = [
        (fighter.id, fighter.lastname + ", " + fighter.firstname)
        for fighter in persons.get_fighters()
    ]
    form.winner.choices = [(-1, "Draw")] + [
        (fighter.id, fighter.lastname + ", " + fighter.firstname)
        for fighter in persons.get_fighters()
    ]
    form.referee.choices = [
        (referee.id, referee.lastname + ", " + referee.firstname)
        for referee in persons.get_referees()
    ]
    form.event.choices = [(-1, "N/A")] + [
        (event.id, event.name) for event in matches.get_events()
    ]
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
    if not matches.get_fight(fight_id):
        flash("Fight not found")
        return redirect("/fights")
    fight = matches.get_fight(fight_id)
    form = FightForm()
    form.fighter1.choices = [
        (fighter.id, fighter.lastname + ", " + fighter.firstname)
        for fighter in persons.get_fighters()
    ]
    form.fighter2.choices = [
        (fighter.id, fighter.lastname + ", " + fighter.firstname)
        for fighter in persons.get_fighters()
    ]
    form.winner.choices = [(-1, "Draw")] + [
        (fighter.id, fighter.lastname + ", " + fighter.firstname)
        for fighter in persons.get_fighters()
    ]
    form.referee.choices = [
        (referee.id, referee.lastname + ", " + referee.firstname)
        for referee in persons.get_referees()
    ]
    form.event.choices = [(-1, "N/A")] + [
        (event.id, event.name) for event in matches.get_events()
    ]
    form.weight_class.choices = persons.get_weight_classes()
    final_round = matches.final_round(fight.ending_time.strftime("%M:%S"))
    ending_time = matches.ending_time(
        final_round, fight.ending_time.strftime("%M:%S"))
    minutes = ending_time.strftime("%M")
    seconds = ending_time.strftime("%S")
    if request.method == "POST" and form.validate_on_submit():
        matches.edit_fight(form, fight_id)
        flash("Fight info updated")
        return redirect("/fights/edit/" + str(fight_id))
    return render_template(
        "add_fight.html",
        form=form,
        fight=fight,
        final_round=final_round,
        minutes=minutes,
        seconds=seconds,
    )


@app.route("/fights/delete/<int:fight_id>")
def delete_fight(fight_id):
    if not users.authorize():
        flash("You are not authorized to delete fights")
        return redirect("/fights/" + str(fight_id))
    if not matches.get_fight(fight_id):
        flash("Fight not found")
        return redirect("/fights")
    matches.delete_fight(fight_id)
    flash("Fight deleted")
    return redirect("/fights")


@app.route("/fights/<int:fight_id>")
def fight_detail(fight_id):
    fight = matches.get_fight(fight_id)
    if fight:
        final_round = matches.final_round(fight.ending_time.strftime("%M:%S"))
        ending_time = matches.ending_time(
            final_round, fight.ending_time.strftime("%M:%S")
        )
        userscore = users.get_score(fight_id, session.get("user_id"))
        popular_scores = users.get_popular_scores(fight_id)
        all_scores = users.get_all_scores(fight_id, True)
        return render_template(
            "fight.html",
            fight=fight,
            is_admin=users.authorize(),
            final_round=final_round,
            ending_time=ending_time,
            is_user=session.get("user_id"),
            userscore=userscore,
            popular_scores=popular_scores,
            all_scores=all_scores,
        )
    else:
        flash("Fight not found")
        return redirect("/fights")


@app.route("/referees/")
def referees_route():
    referees = persons.get_referee_list()
    return render_template("referees.html", count=len(referees), referees=referees)


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
    return render_template("add_official.html", form=form, is_new=True)


@app.route("/referees/<int:referee_id>")
def referee_profile(referee_id):
    referee = persons.get_referee(referee_id)
    fights = matches.fights_by_id("referee", referee_id)
    if referee:
        return render_template(
            "referee.html", referee=referee, fights=fights, is_admin=users.authorize()
        )
    else:
        flash("Referee not found")
        return redirect("/referees")


@app.route("/referees/edit/<int:referee_id>", methods=["GET", "POST"])
def edit_referee(referee_id):
    if not users.authorize():
        flash("You are not authorized to edit referees")
        return redirect("/referees/" + str(referee_id))
    referee = persons.get_referee(referee_id)
    if not referee:
        flash("Referee not found")
        return redirect("/referees")
    form = OfficialsForm()
    if request.method == "POST" and form.validate_on_submit():
        persons.edit_referee(form, referee_id)
        flash("Referee info updated")
        return redirect("/referees/edit/" + str(referee_id))
    return render_template("add_official.html", form=form, referee=referee)


@app.route("/referees/delete/<int:referee_id>")
def delete_referee(referee_id):
    if not users.authorize():
        flash("You are not authorized to delete referees")
        return redirect("/referees/" + str(referee_id))
    if not persons.get_referee(referee_id) or referee_id == 1:
        flash("Referee not found")
        return redirect("/referees")
    persons.delete_referee(referee_id)
    flash("Referee deleted")
    return redirect("/referees")


@app.route("/events/", methods=["GET", "POST"])
def events_route():
    events = matches.get_events()
    return render_template("events.html", count=len(events), events=events)


@app.route("/events/<int:event_id>")
def event_detail(event_id):
    event = matches.get_event(event_id)
    fights = matches.get_fightlist(event_id)
    final_rounds = [
        matches.final_round(fight.ending_time.strftime("%M:%S")) for fight in fights
    ]
    ending_times = [
        matches.ending_time(final_round, fight.ending_time.strftime("%M:%S"))
        for final_round, fight in zip(final_rounds, fights)
    ]
    if event:
        return render_template(
            "event.html",
            event=event,
            fights=fights,
            final_rounds=final_rounds,
            ending_times=ending_times,
            is_admin=users.authorize(),
        )
    else:
        flash("Event not found")
        return redirect("/events")


@app.route("/events/new", methods=["GET", "POST"])
def add_event():
    if not users.authorize():
        flash("You are not authorized to add events")
        return redirect("/events")
    form = EventForm()
    if request.method == "POST" and form.validate_on_submit():
        if matches.add_event(form):
            flash("Event added successfully")
        else:
            flash("Event already exists")
    return render_template("add_event.html", form=form, is_new=True)


@app.route("/events/edit/<int:event_id>", methods=["GET", "POST"])
def edit_event(event_id):
    if not users.authorize():
        flash("You are not authorized to edit events")
        return redirect("/events/" + str(event_id))
    event = matches.get_event(event_id)
    if not event:
        flash("Event not found")
        return redirect("/events")
    form = EventForm()
    if request.method == "POST" and form.validate_on_submit():
        matches.edit_event(form, event_id)
        flash("Event info updated")
        return redirect("/events/edit/" + str(event_id))
    return render_template("add_event.html", form=form, event=event)


@app.route("/events/delete/<int:event_id>", methods=["GET", "POST"])
def delete_event(event_id):
    if not users.authorize():
        flash("You are not authorized to delete events")
        return redirect("/events/" + str(event_id))
    if not matches.get_event(event_id):
        flash("Event not found")
        return redirect("/events")
    if request.method == "POST":
        matches.delete_event(event_id)
        flash("Event deleted")
    return redirect("/events")


@app.route("/fights/<int:fight_id>/new/<int:user_id>", methods=["GET", "POST"])
def add_score(fight_id, user_id):
    if not session.get("user_id"):
        flash("You must register or login to add scores")
        return redirect("/fights/" + str(fight_id))
    if not session.get("user_id") == user_id:
        flash("Action not authorized")
        return redirect("/fights/" + str(fight_id))
    fight = matches.get_fight(fight_id)
    if not fight:
        flash("Fight not found")
        return redirect("/fights")
    form = ScoreForm()
    if request.method == "POST" and form.validate_on_submit():
        check_score = matches.check_score(form, fight)
        if check_score == "error1":
            flash("Please give a score for both fighters.")
            return redirect("/fights/" + str(fight_id) + "/new/" + str(id))
        elif check_score == "error2":
            flash(
                "You can't score more than 30 points for a fighter in a 3 round fight, please check your score.")
            return redirect("/fights/" + str(fight_id) + "/new/" + str(id))
        if check_score:
            flash(check_score)
        if matches.score_fight(form, fight_id, user_id):
            flash("Score added successfully")
        else:
            flash("You have already scored this fight, did you mean to edit?")
        return redirect("/fights/" + str(fight_id))
    return render_template(
        "add_score.html",
        form=form,
        fight=fight,
        user_id=user_id,
        is_new=True,
    )


@app.route("/fights/<int:fight_id>/edit/<int:user_id>", methods=["GET", "POST"])
def edit_score(fight_id, user_id):
    if session.get("user_id") != user_id and not users.is_admin(session.get("user_id")):
        flash("Action not authorized")
        return redirect("/fights/" + str(fight_id))
    fight = matches.get_fight(fight_id)
    if not fight:
        flash("Fight not found")
        return redirect("/fights")
    score = users.get_score(fight_id, user_id)
    if not score:
        flash("You have not scored this fight yet")
        return redirect("/fights/" + str(fight_id))
    form = ScoreForm()
    if request.method == "POST" and form.validate_on_submit():
        check_score = matches.check_score(form, fight)
        if check_score == "error1":
            flash("Please give a score for both fighters.")
            return redirect("/fights/" + str(fight_id) + "/edit/" + str(id))
        elif check_score == "error2":
            flash(
                "You can't score more than 30 points for a fighter in a 3 round fight, please check your score.")
            return redirect("/fights/" + str(fight_id) + "/edit/" + str(id))
        if check_score:
            flash(check_score)
        matches.edit_score(form, score.id)
        flash("Score updated")
        return redirect("/fights/" + str(fight_id))
    return render_template(
        "add_score.html",
        form=form,
        fight=fight,
        user_id=user_id,
        score=score,
    )


@app.route("/fights/<int:fight_id>/delete/<int:user_id>", methods=["GET", "POST"])
def delete_score(fight_id, user_id):
    if session.get("user_id") != user_id and not users.is_admin(session.get("user_id")):
        flash("Action not authorized")
        return redirect("/fights/" + str(fight_id))
    score = users.get_score(fight_id, user_id)
    if not score:
        flash("You have not scored this fight")
        return redirect("/fights/" + str(fight_id))
    score = users.get_score(fight_id, user_id)
    if request.method == "POST":
        matches.delete_score(score.id)
        flash("Score deleted")
    return redirect("/fights/" + str(fight_id))


@app.route("/fights/<int:fight_id>/scorecards/")
def scorecards(fight_id):
    fight = matches.get_fight(fight_id)
    if not fight:
        flash("Fight not found")
        return redirect("/fights")
    scores = users.get_all_scores(fight_id, False)
    final_round = matches.final_round(fight.ending_time.strftime("%M:%S"))
    ending_time = matches.ending_time(
        final_round, fight.ending_time.strftime("%M:%S")
    )
    return render_template(
        "scorecards.html",
        fight=fight,
        scores=scores,
        final_round=final_round,
        ending_time=ending_time,
        is_admin=users.is_admin(session.get("user_id")),
    )
