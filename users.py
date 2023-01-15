from db import db
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash
import os


def login(username, password):
    sql = "SELECT id, password FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username": username})
    user = result.fetchone()
    
    if not user:
        return False
    else:
        password_hash = user.password
        if check_password_hash(password_hash, password):
            session["user_id"] = user.id
            return True
        else:
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
    user = result.fetchone()
    if user:    
        return user.admin


def authorize():
    if not session.get("user_id"):
        return False
    if not is_admin(session["user_id"]):
        return False
    return True
