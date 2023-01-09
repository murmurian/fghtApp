from db import db
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash
import os

def is_admin(user_id):
    result = db.session.execute(
        "SELECT admin FROM users WHERE id = :id", {"id": user_id})
    user = result.fetchone()
    return user.admin
