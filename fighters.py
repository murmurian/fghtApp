from db import db
from flask import session


def get_fighters():
    result = db.session.execute(
        "SELECT * FROM fighters")
    return result.fetchall()
