from app import app
from db import db
from flask import redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash
import users


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    username = request.form["username"]
    password = request.form["password"]
    sql = "SELECT id, password FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username": username})
    user = result.fetchone()
    if not user:
        return render_template("error.html", message="No such username or password")
    else:
        password_hash = user.password
        if check_password_hash(password_hash, password):
            session["user_id"] = user.id
            return redirect("/")
        else:
            return render_template("error.html", message="No such username or password")


@app.route("/logout")
def logout():
    del session["user_id"]
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    username = request.form["username"]
    password = request.form["password"]
    password_hash = generate_password_hash(password)
    sql = "INSERT INTO users (username, password, admin) VALUES (:username, :password)"
    db.session.execute(sql, {"username": username, "password": password_hash})
    db.session.commit()
    return redirect("/")


@app.route("/fighters")
def fighters():
    result = db.session.execute(
        "SELECT fighters.*, countries.name AS country_name, EXTRACT(YEAR FROM CURRENT_DATE) - EXTRACT(YEAR FROM born) AS age FROM fighters JOIN countries ON fighters.country = countries.id")
    fighters = result.fetchall()
    return render_template("fighters.html", count=len(fighters), messages=fighters)


@app.route("/add_fighter", methods=["GET", "POST"])
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

