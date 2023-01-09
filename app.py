from flask import Flask
from flask import redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash
from os import getenv

app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
db = SQLAlchemy(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login",methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    # TODO: check username and password
    session["username"] = username
    return redirect("/")

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")

@app.route("/fighters")
def fighters():
    result = db.session.execute("SELECT * FROM fighters")
    fighters = result.fetchall()
    return render_template("fighters.html", count=len(fighters), messages=fighters)

@app.route("/add_fighter")
def add_fighter():
    result = db.session.execute("SELECT name FROM countries")
    countries = result.fetchall()

    return render_template("add_fighter.html", countries=countries)

@app.route("/send", methods=["POST"])
def send():
    firstname = request.form["firstname"]
    lastname = request.form["lastname"]
    nickname = request.form["nickname"]
    born = request.form["born"]
    height = request.form["height"]
    weight = request.form["weight"]
    country_name = request.form["country"]

    # Look up the country id based on the country name
    result = db.session.execute("SELECT id FROM countries WHERE name = :name", {"name": country_name})
    country_id = result.fetchone()[0]

    # Insert a new row into the fighters table
    db.session.execute(sql, {"firstname": firstname, "lastname": lastname, "nickname": nickname, "born": born, "height": height, "weight": weight, "country": country_id})
    db.session.commit()

    return redirect("/")

