from db import db


def get_countries():
    result = db.session.execute(
        "SELECT * FROM countries")
    return result.fetchall()