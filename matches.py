from datetime import time
from db import db


def get_countries():
    result = db.session.execute("SELECT * FROM countries")
    return result.fetchall()


def fights_by_id(role, id):
    sql = """SELECT f.*,
        f1.firstname AS f1_firstname, f1.lastname AS f1_lastname, f1.nickname AS f1_nickname,
        f2.firstname AS f2_firstname, f2.lastname AS f2_lastname, f2.nickname AS f2_nickname,
        r.firstname AS r_firstname, r.lastname AS r_lastname, e.name AS event_name
        FROM fights f
        LEFT JOIN fighters f1 ON f.fighter1 = f1.id
        LEFT JOIN fighters f2 ON f.fighter2 = f2.id
        LEFT JOIN referees r ON f.referee = r.id
        LEFT JOIN events e ON f.event = e.id"""
    if role == "referee":
        sql += " WHERE f.referee = :id"
    if role == "fighter":
        sql += " WHERE f.fighter1 = :id OR f.fighter2 = :id"
    sql += " ORDER BY f.date"
    result = db.session.execute(sql, {"id": id})
    return result.fetchall()


def get_fightlist(event_id):
    sql = """SELECT f.*,
        f1.firstname AS f1_firstname, f1.lastname AS f1_lastname,
        f2.firstname AS f2_firstname, f2.lastname AS f2_lastname,
        r.firstname AS r_firstname, r.lastname AS r_lastname, e.name AS event_name
        FROM fights f
        LEFT JOIN fighters f1 ON f.fighter1 = f1.id
        LEFT JOIN fighters f2 ON f.fighter2 = f2.id
        LEFT JOIN referees r ON f.referee = r.id
        LEFT JOIN events e ON f.event = e.id"""
    if event_id:
        sql += " WHERE f.event = :event_id ORDER BY fight_order DESC"
    else:
        sql += " ORDER BY f.date DESC LIMIT 10"

    result = db.session.execute(sql, {"event_id": event_id})
    return result.fetchall()


def add_fight(form):
    fighter1 = form.fighter1.data
    fighter2 = form.fighter2.data
    referee = form.referee.data
    rounds = form.rounds.data
    ending_time = calculate_ending_time(form)
    if form.winner.data == -1:
        winner = None
        draw = True
    else:
        winner = form.winner.data
        draw = False
    method = form.winning_method.data
    date = form.date.data
    if form.event.data == -1:
        event = None
    else:
        event = form.event.data
    fight_order = form.fight_order.data
    weight_class = form.weight_class.data

    sql = "SELECT * FROM fights WHERE (fighter1 = :fighter1 AND fighter2 = :fighter2) OR (fighter1 = :fighter2 AND fighter2 = :fighter1) AND date = :date"
    existing_fight = db.session.execute(
        sql, {"fighter1": fighter1, "fighter2": fighter2, "date": date}
    ).fetchone()
    if existing_fight:
        return False

    sql = "INSERT INTO fights (fighter1, fighter2, referee, rounds, ending_time, winner, draw, winning_method, date, event, fight_order, weight_class) VALUES (:fighter1, :fighter2, :referee, :rounds, :ending_time, :winner, :draw, :method, :date, :event, :fight_order, :weight_class)"
    db.session.execute(
        sql,
        {
            "fighter1": fighter1,
            "fighter2": fighter2,
            "referee": referee,
            "rounds": rounds,
            "ending_time": ending_time,
            "winner": winner,
            "draw": draw,
            "method": method,
            "date": date,
            "event": event,
            "fight_order": fight_order,
            "weight_class": weight_class,
        },
    )
    db.session.commit()
    return True


def edit_fight(form, fight_id):
    fighter1 = form.fighter1.data
    fighter2 = form.fighter2.data
    referee = form.referee.data
    rounds = form.rounds.data
    ending_time = calculate_ending_time(form)
    draw = False
    if form.winner.data == -1:
        winner = None
        draw = True
    else:
        winner = form.winner.data
    method = form.winning_method.data
    date = form.date.data
    if form.event.data == -1:
        event = None
    else:
        event = form.event.data
    fight_order = form.fight_order.data
    weight_class = form.weight_class.data

    sql = "UPDATE fights SET fighter1 = :fighter1, fighter2 = :fighter2, referee = :referee, rounds = :rounds, ending_time = :ending_time, winner = :winner, draw = :draw, winning_method = :method, date = :date, event = :event, fight_order = :fight_order, weight_class = :weight_class WHERE id = :fight_id"
    db.session.execute(
        sql,
        {
            "fighter1": fighter1,
            "fighter2": fighter2,
            "referee": referee,
            "rounds": rounds,
            "ending_time": ending_time,
            "winner": winner,
            "draw": draw,
            "method": method,
            "date": date,
            "event": event,
            "fight_order": fight_order,
            "weight_class": weight_class,
            "fight_id": fight_id,
        },
    )
    db.session.commit()


def delete_fight(fight_id):
    sql = "DELETE FROM fights WHERE id = :fight_id"
    db.session.execute(sql, {"fight_id": fight_id})
    db.session.commit()


def get_fight(fight_id):
    sql = """SELECT f.*,
        f1.firstname AS f1_firstname, f1.lastname AS f1_lastname, f1.nickname AS f1_nickname,
        f2.firstname AS f2_firstname, f2.lastname AS f2_lastname, f2.nickname AS f2_nickname,
        w.firstname AS w_firstname, w.lastname AS w_lastname,
        r.firstname AS r_firstname, r.lastname AS r_lastname, e.name AS event_name
        FROM fights f
        LEFT JOIN fighters f1 ON f.fighter1 = f1.id
        LEFT JOIN fighters f2 ON f.fighter2 = f2.id
        LEFT JOIN fighters w ON f.winner = w.id
        LEFT JOIN referees r ON f.referee = r.id
        LEFT JOIN events e ON f.event = e.id
        WHERE f.id = :fight_id"""
    result = db.session.execute(sql, {"fight_id": fight_id}).fetchone()
    return result


def get_events():
    result = db.session.execute("SELECT * FROM events")
    return result.fetchall()


def get_event(event_id):
    sql = "SELECT * FROM events WHERE id = :event_id"
    result = db.session.execute(sql, {"event_id": event_id})
    return result.fetchone()


def add_event(form):
    name = form.name.data.strip().upper()
    date = form.date.data
    location = form.location.data.strip()
    promotion = form.promotion.data.strip()

    sql = "SELECT * FROM events WHERE name = :name"
    existing_event = db.session.execute(sql, {"name": name}).fetchone()
    if existing_event:
        return False

    sql = "INSERT INTO events (name, date, location, promotion) VALUES (:name, :date, :location, :promotion)"
    db.session.execute(
        sql, {"name": name, "date": date,
              "location": location, "promotion": promotion}
    )
    db.session.commit()
    return True


def edit_event(form, event_id):
    name = form.name.data.strip().upper()
    date = form.date.data
    location = form.location.data.strip()
    promotion = form.promotion.data.strip()

    sql = "UPDATE events SET name = :name, date = :date, location = :location, promotion = :promotion WHERE id = :event_id"
    db.session.execute(
        sql,
        {
            "name": name,
            "date": date,
            "location": location,
            "promotion": promotion,
            "event_id": event_id,
        },
    )
    db.session.commit()


def delete_event(event_id):
    sql = "DELETE FROM events WHERE id = :event_id"
    db.session.execute(sql, {"event_id": event_id})
    db.session.commit()


def get_fights(event_id):
    sql = "SELECT * FROM fights WHERE event = :event_id"
    result = db.session.execute(sql, {"event_id": event_id})
    return result.fetchall()


def score_fight(form, fight_id, id):
    sql = "SELECT * FROM scorecards WHERE fight = :fight_id AND username = :id"
    existing_score = db.session.execute(
        sql, {"fight_id": fight_id, "id": id}
    ).fetchone()
    if existing_score:
        return False
    score_f1 = form.score_f1.data
    score_f2 = form.score_f2.data
    comment = form.comment.data
    sql = "INSERT INTO scorecards (username, fight, score_f1, score_f2, comment) VALUES (:username, :fight, :score_f1, :score_f2, :comment)"
    db.session.execute(
        sql,
        {
            "username": id,
            "fight": fight_id,
            "score_f1": score_f1,
            "score_f2": score_f2,
            "comment": comment,
        },
    )
    db.session.commit()
    return True


def edit_score(form, score_id):
    score_f1 = form.score_f1.data
    score_f2 = form.score_f2.data
    comment = form.comment.data
    sql = "UPDATE scorecards SET score_f1 = :score_f1, score_f2 = :score_f2, comment = :comment WHERE id = :score_id"
    db.session.execute(
        sql,
        {
            "score_f1": score_f1,
            "score_f2": score_f2,
            "comment": comment,
            "score_id": score_id,
        },
    )
    db.session.commit()


def check_score(form, fight):
    if (
        (fight.rounds == 5 and fight.ending_time.strftime("%M:%S") != "25:00")
        or (fight.rounds == 3 and fight.ending_time.strftime("%M:%S") != "15:00")
    ) and (form.score_f1.data or form.score_f2.data):
        return "Fight did not end in full time, please leave a comment instead."
    if not form.score_f1.data and not form.score_f2.data:
        return
    if fight.rounds == 5:
        if form.score_f1.data + form.score_f2.data > 95:
            return "10-10 rounds are extremely rare, please check your score."
        if form.score_f1.data < 42 or form.score_f2.data < 42:
            return "Your score for one of the fighters is very low, please check your score.\nRounds below 10-8 are extremely rare."
    if fight.rounds == 3:
        if form.score_f1.data > 30 or form.score_f2.data > 30:
            return "error"
        if form.score_f1.data + form.score_f2.data > 57:
            return "10-10 rounds are extremely rare, please check your score."
        if form.score_f1.data < 25 or form.score_f2.data < 25:
            return "Your score for one of the fighters is very low, please check your score.\nRounds below 10-8 are extremely rare."


def delete_score(score_id):
    sql = "DELETE FROM scorecards WHERE id = :score_id"
    db.session.execute(sql, {"score_id": score_id})
    db.session.commit()


def calculate_ending_time(form):
    round = form.ending_round.data
    minutes = form.minutes.data
    seconds = form.seconds.data
    ending_time = time(hour=0, minute=minutes +
                       (round - 1) * 5, second=seconds)
    return ending_time


def final_round(ending_time):
    minutes = int(ending_time[0:2])
    if minutes % 5 == 0:
        return minutes // 5
    return minutes // 5 + 1


def ending_time(final_round, ending_time):
    minutes = int(ending_time[0:2])
    seconds = int(ending_time[3:5])
    minutes = minutes - ((final_round - 1) * 5)
    return time(hour=0, minute=minutes, second=seconds)
