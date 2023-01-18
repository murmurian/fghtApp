from db import db


def get_fighters():
    result = db.session.execute(
        "SELECT * FROM fighters ORDER BY lastname")
    return result.fetchall()


def get_fighter(id):
    sql = "SELECT f.*, c.id AS country_id, c.name AS country_name FROM fighters f JOIN countries c ON f.country = c.id WHERE f.id = :id"
    result = db.session.execute(sql, {"id": id}).fetchone()
    return result


def get_referees():
    result = db.session.execute(
        "SELECT * FROM referees ORDER BY lastname")
    return result.fetchall()


def add_fighter(form):
    firstname = form.firstname.data
    lastname = form.lastname.data
    nickname = form.nickname.data
    born = form.born.data
    height = format_height(form.feet.data, form.inches.data)
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


def edit_fighter(form, fighter_id):
    firstname = form.firstname.data
    lastname = form.lastname.data
    nickname = form.nickname.data
    born = form.born.data
    height = format_height(form.feet.data, form.inches.data)
    weight = form.weight.data
    country = form.country.data

    sql = "UPDATE fighters SET firstname = :firstname, lastname = :lastname, nickname = :nickname, born = :born, height = :height, weight = :weight, country = :country WHERE id = :id"
    db.session.execute(sql, {"firstname": firstname, "lastname": lastname, "nickname": nickname,
                       "born": born, "height": height, "weight": weight, "country": country, "id": fighter_id})
    db.session.commit()


def delete_fighter(id):
    sql = "DELETE FROM fighters WHERE id = :id"
    db.session.execute(sql, {"id": id})
    db.session.commit()


def get_fighter_id(firstname, lastname, born):
    sql = "SELECT id FROM fighters WHERE firstname = :firstname AND lastname = :lastname AND born = :born"
    result = db.session.execute(sql, {"firstname": firstname, "lastname": lastname, "born": born}).fetchone()
    return result[0]


def add_referee(form):
    firstname = form.firstname.data
    lastname = form.lastname.data
    
    sql = "SELECT * FROM referees WHERE firstname = :firstname AND lastname = :lastname"
    existing_referee = db.session.execute(sql, {"firstname": firstname, "lastname": lastname}).fetchone()
    if existing_referee:
        return False

    sql = "INSERT INTO referees (firstname, lastname) VALUES (:firstname, :lastname)"
    db.session.execute(sql, {"firstname": firstname, "lastname": lastname})
    db.session.commit()
    return True


def get_weight_classes():
    weight_classes = [(115, "Strawweight"), (125, "Flyweight"), (135, "Bantamweight"), (145, "Featherweight"), (155, "Lightweight"), (170, "Welterweight"), (185, "Middleweight"), (205, "Light Heavyweight"), (265, "Heavyweight"), (115, "Women's Strawweight"), (125, "Women's Flyweight"),
                      (135, "Women's Bantamweight"), (145, "Women's Featherweight"), (155, "Women's Lightweight"), (0, "Catchweight"), (500, "Open Weight")]
    return weight_classes


def format_height(feet, inches):
    return str(feet) + "." + str(inches)
