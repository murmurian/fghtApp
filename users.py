from flask import session
from werkzeug.security import check_password_hash, generate_password_hash
from db import db


def login(username, password):
    sql = "SELECT id, password FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username": username})
    user = result.fetchone()
    if not user:
        return False
    password_hash = user.password
    if check_password_hash(password_hash, password):
        session["user_id"] = user.id
        return True
    return False


def register(username, password):
    sql = "SELECT username FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username": username})
    duplicate_user = result.fetchone()
    if duplicate_user:
        return False
    password_hash = generate_password_hash(password)
    sql = "INSERT INTO users (username, password) VALUES (:username, :password)"
    db.session.execute(sql, {"username": username, "password": password_hash})
    db.session.commit()
    return True


def is_admin(user_id):
    result = db.session.execute(
        "SELECT admin FROM users WHERE id = :id", {"id": user_id})
    return result.fetchone().admin


def authorize():
    if not session.get("user_id"):
        return False
    if not is_admin(session["user_id"]):
        return False
    return True


def get_score(fight_id, user_id):
    sql = "SELECT * FROM scorecards WHERE fight=:fight_id AND username=:user_id"
    result = db.session.execute(
        sql, {"fight_id": fight_id, "user_id": user_id})
    return result.fetchone()


def get_all_scores(fight_id):
    sql = """SELECT score_f1, score_f2, COUNT(*) as count
        FROM scorecards
        WHERE fight = :fight_id
        GROUP BY score_f1, score_f2
        ORDER BY count
        DESC LIMIT 5;"""
    result = db.session.execute(sql, {"fight_id": fight_id})
    return result.fetchall()


def get_random_comments(fight_id):
    sql = "SELECT comment FROM scorecards WHERE fight=:fight_id ORDER BY RANDOM LIMIT 3"
    result = db.session.execute(sql, {"fight_id": fight_id})
    return result.fetchall()


def get_all_comments(fight_id):
    sql = "SELECT comment FROM scorecards WHERE fight=:fight_id"
    result = db.session.execute(sql, {"fight_id": fight_id})
    return result.fetchall()
