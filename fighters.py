from db import db


def get_fighters():
    result = db.session.execute(
        "SELECT * FROM fighters")
    return result.fetchall()


def get_fighter(id):
    sql = "SELECT f.id, f.firstname, f.lastname, f.nickname, f.born, f.height, f.weight, c.name as country FROM fighters f JOIN countries c ON f.country = c.id WHERE f.id = :id"
    result = db.session.execute(sql, {"id": id}).fetchone()
    return result


def add_fighter(form):
    firstname = form.firstname.data
    lastname = form.lastname.data
    nickname = form.nickname.data
    born = form.born.data
    height = form.height.data
    weight = form.weight.data
    country = form.country.data

    sql = "SELECT * FROM fighters WHERE firstname = :firstname AND lastname = :lastname AND born = :born"
    existing_fighter = db.session.execute(
        sql, {"firstname": firstname, "lastname": lastname, "born": born}).fetchone()
    if existing_fighter:
        return False

    sql = "INSERT INTO fighters (firstname, lastname, nickname, born, height, weight, country) VALUES (:firstname, :lastname, :nickname, :born, :height, :weight, :country)"
    db.session.execute(sql, {"firstname": firstname, "lastname": lastname, "nickname": nickname,
                       "born": born, "height": height, "weight": weight, "country": country})

    db.session.commit()
    return True
