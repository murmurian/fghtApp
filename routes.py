from app import app
from db import db
from flask import redirect, render_template, request, session
from forms import RegistrationForm, SearchForm
import users, fighters, forms, fights


@app.route("/")
def index():
    return render_template("index.html", session=session, users=users)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html", session=session, users=users)
    username = request.form["username"]
    password = request.form["password"]
    if users.login(username, password):
        return redirect("/")
    return render_template("error.html", message="No such username or password", session=session, users=users)


@app.route("/logout")
def logout():
    del session["user_id"]
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        if not users.register(username, password):
            return render_template("error.html", message="Username already registered", session=session, users=users)
        return redirect("/login")
    return render_template("register.html", form=form, session=session, users=users)


@app.route("/fighters", methods=["GET", "POST"])
def fighters_route():
    form = SearchForm()
    if request.method == "POST" and form.validate_on_submit() and form.q.data:
        print("Hi!")
        query = form.q.data
        sql = "SELECT fighters.*, countries.name AS country_name, EXTRACT(YEAR FROM CURRENT_DATE) - EXTRACT(YEAR FROM born) AS age FROM fighters JOIN countries ON fighters.country = countries.id WHERE fighters.firstname like :query or fighters.lastname like :query or countries.name like :query"
        result = db.session.execute(sql, {"query": '%'+query+'%'})
    else:
        result = db.session.execute("SELECT fighters.*, countries.name AS country_name, EXTRACT(YEAR FROM CURRENT_DATE) - EXTRACT(YEAR FROM born) AS age FROM fighters JOIN countries ON fighters.country = countries.id")
    fighters = result.fetchall()
    return render_template("fighters.html", count=len(fighters), messages=fighters, form=form, session=session, users=users)



@app.route("/fighters/new", methods=["GET", "POST"])
def add_fighter():
    if "user_id" not in session or not users.is_admin(session["user_id"]):
        return redirect("/login")

    if request.method == "GET":
        result = db.session.execute("SELECT name FROM countries")
        countries = result.fetchall()
        return render_template("add_fighter.html", countries=countries)

    firstname = request.form["firstname"]
    lastname = request.form["lastname"]
    nickname = request.form["nickname"]
    born = request.form["born"]
    height = request.form["height"]
    weight = request.form["weight"]
    country_name = request.form["country"]

    # Look up the country id based on the country name
    result = db.session.execute(
        "SELECT id FROM countries WHERE name = :name", {"name": country_name})
    country_id = result.fetchone()[0]

    # Insert a new row into the fighters table
    sql = "INSERT INTO fighters (firstname, lastname, nickname, born, height, weight, country) VALUES (:firstname, :lastname, :nickname, :born, :height, :weight, :country)"
    db.session.execute(sql, {"firstname": firstname, "lastname": lastname, "nickname": nickname,
                             "born": born, "height": height, "weight": weight, "country": country_id})
    db.session.commit()

    return redirect("/")


@app.route("/fights")
def fights_route():
    result = db.session.execute(
        "SELECT fights.*, f1.firstname as f1_firstname, f1.lastname as f1_lastname, f2.firstname as f2_firstname, f2.lastname as f2_lastname, r.firstname as ref_firstname, r.lastname as ref_lastname FROM fights JOIN fighters f1 ON f1.id = fights.fighter1 JOIN fighters f2 ON f2.id = fights.fighter2 JOIN referees r ON r.id = fights.referee")
    fights = result.fetchall()
    return render_template("fights.html", count=len(fights), fights=fights)

