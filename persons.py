from db import db


def get_fighters():
    result = db.session.execute("SELECT * FROM fighters ORDER BY lastname")
    return result.fetchall()


def get_random_fighters():
    result = db.session.execute("SELECT fighters.*, countries.name AS country_name FROM fighters JOIN countries ON fighters.country = countries.id ORDER BY RANDOM() LIMIT 10")
    return result.fetchall()


def search_fighters(form):
    parts = form.search.data.split()
    if not parts:
        return get_random_fighters()
    if len(parts) == 1:
        sql = "SELECT fighters.*, countries.name AS country_name FROM fighters JOIN countries ON fighters.country = countries.id WHERE firstname ILIKE :search OR lastname ILIKE :search OR nickname ILIKE :search ORDER BY firstname"
        result = db.session.execute(sql, {"search": f"%{form.search.data}%"})
    else:
        sql = "SELECT fighters.*, countries.name AS country_name FROM fighters JOIN countries ON fighters.country = countries.id WHERE (firstname ILIKE :search1 AND lastname ILIKE :search2) OR (firstname ILIKE :search2 AND lastname ILIKE :search1) ORDER BY firstname"
        result = db.session.execute(sql, {"search1": f"%{parts[0]}%", "search2": f"%{parts[1]}%"})
    return result.fetchall()
    

def get_fighter(id):
    sql = "SELECT f.*, c.id AS country_id, c.name AS country_name FROM fighters f JOIN countries c ON f.country = c.id WHERE f.id = :id"
    result = db.session.execute(sql, {"id": id}).fetchone()
    return result


def get_referees():
    result = db.session.execute("SELECT * FROM referees ORDER BY lastname")
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
        sql, {"firstname": firstname, "lastname": lastname, "born": born}
    ).fetchone()
    if existing_fighter:
        return False

    sql = "INSERT INTO fighters (firstname, lastname, nickname, born, height, weight, country) VALUES (:firstname, :lastname, :nickname, :born, :height, :weight, :country)"
    db.session.execute(
        sql,
        {
            "firstname": firstname,
            "lastname": lastname,
            "nickname": nickname,
            "born": born,
            "height": height,
            "weight": weight,
            "country": country,
        },
    )

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
    db.session.execute(
        sql,
        {
            "firstname": firstname,
            "lastname": lastname,
            "nickname": nickname,
            "born": born,
            "height": height,
            "weight": weight,
            "country": country,
            "id": fighter_id,
        },
    )
    db.session.commit()


def delete_fighter(id):
    sql = "DELETE FROM fighters WHERE id = :id"
    db.session.execute(sql, {"id": id})
    db.session.commit()


def get_fighter_id(firstname, lastname, born):
    sql = "SELECT id FROM fighters WHERE firstname = :firstname AND lastname = :lastname AND born = :born"
    result = db.session.execute(
        sql, {"firstname": firstname, "lastname": lastname, "born": born}
    ).fetchone()
    return result[0]


def get_referee(id):
    sql = "SELECT * FROM referees WHERE id = :id"
    result = db.session.execute(sql, {"id": id}).fetchone()
    return result


def add_referee(form):
    firstname = form.firstname.data
    lastname = form.lastname.data

    sql = "SELECT * FROM referees WHERE firstname = :firstname AND lastname = :lastname"
    existing_referee = db.session.execute(
        sql, {"firstname": firstname, "lastname": lastname}
    ).fetchone()
    if existing_referee:
        return False

    sql = "INSERT INTO referees (firstname, lastname) VALUES (:firstname, :lastname)"
    db.session.execute(sql, {"firstname": firstname, "lastname": lastname})
    db.session.commit()
    return True


def edit_referee(form, referee_id):
    firstname = form.firstname.data
    lastname = form.lastname.data

    sql = "UPDATE referees SET firstname = :firstname, lastname = :lastname WHERE id = :id"
    db.session.execute(
        sql, {"firstname": firstname, "lastname": lastname, "id": referee_id}
    )
    db.session.commit()


def delete_referee(id):
    sql = "DELETE FROM referees WHERE id = :id"
    db.session.execute(sql, {"id": id})
    db.session.commit()


def get_referee_list():
    result = db.session.execute("SELECT * FROM referees WHERE id > 1 Order BY lastname")
    return result.fetchall()


def get_weight_classes():
    weight_classes = [
        (115, "Strawweight"),
        (125, "Flyweight"),
        (135, "Bantamweight"),
        (145, "Featherweight"),
        (155, "Lightweight"),
        (170, "Welterweight"),
        (185, "Middleweight"),
        (205, "Light Heavyweight"),
        (265, "Heavyweight"),
        (115, "Women's Strawweight"),
        (125, "Women's Flyweight"),
        (135, "Women's Bantamweight"),
        (145, "Women's Featherweight"),
        (155, "Women's Lightweight"),
        (100, "Catchweight"),
        (500, "Open Weight"),
    ]
    return weight_classes


def format_height(feet, inches):
    return str(feet) + "." + str(inches)
