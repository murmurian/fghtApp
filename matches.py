from datetime import time, timedelta
from db import db


def get_countries():
    result = db.session.execute(
        "SELECT * FROM countries")
    return result.fetchall()


def get_fights(fighter_id):
    sql = """SELECT f.*,
        f1.firstname AS f1_firstname, f1.lastname AS f1_lastname, f1.nickname AS f1_nickname,
        f2.firstname AS f2_firstname, f2.lastname AS f2_lastname, f2.nickname AS f2_nickname,
        r.firstname AS r_firstname, r.lastname AS r_lastname, e.name AS event_name
        FROM fights f
        LEFT JOIN fighters f1 ON f.fighter1 = f1.id
        LEFT JOIN fighters f2 ON f.fighter2 = f2.id
        LEFT JOIN referees r ON f.referee = r.id
        LEFT JOIN events e ON f.event = e.id
        WHERE f.fighter1 = :fighter_id OR f.fighter2 = :fighter_id
        ORDER BY f.date"""
    result = db.session.execute(sql, {"fighter_id": fighter_id})
    return result.fetchall()


def add_fight(form):
    fighter1 = form.fighter1.data
    fighter2 = form.fighter2.data
    referee = form.referee.data
    rounds = form.rounds.data
    ending_time = calculate_ending_time(form)
    if form.winner.data == "-1":
        winner = None
    else:
        winner = form.winner.data
    method = form.winning_method.data
    date = form.date.data
    if form.event.data == "-1":
        event = None
    else:
        event = form.event.data
    fight_order = form.fight_order.data
    weight_class = form.weight_class.data

    sql = "SELECT * FROM fights WHERE (fighter1 = :fighter1 AND fighter2 = :fighter2) OR (fighter1 = :fighter2 AND fighter2 = :fighter1) AND date = :date"
    existing_fight = db.session.execute(
        sql, {"fighter1": fighter1, "fighter2": fighter2, "date": date}).fetchone()
    if existing_fight:
        return False

    sql = "INSERT INTO fights (fighter1, fighter2, referee, rounds, ending_time, winner, winning_method, date, event, fight_order, weight_class) VALUES (:fighter1, :fighter2, :referee, :rounds, :ending_time, :winner, :method, :date, :event, :fight_order, :weight_class)"
    db.session.execute(sql, {"fighter1": fighter1, "fighter2": fighter2, "referee": referee,
                       "rounds": rounds, "ending_time": ending_time, "winner": winner, "method": method, "date": date, "event": event, "fight_order": fight_order, "weight_class": weight_class})
    db.session.commit()
    return True

def get_events():
    result = db.session.execute(
        "SELECT * FROM events")
    return result.fetchall()


def get_event(event_id):
    sql = "SELECT * FROM events WHERE id = :event_id"
    result = db.session.execute(sql, {"event_id": event_id})
    return result.fetchone()


def get_fights(event_id):
    sql = "SELECT * FROM fights WHERE event = :event_id"
    result = db.session.execute(sql, {"event_id": event_id})
    return result.fetchall()


def calculate_ending_time(form):
    round = form.ending_round.data
    minutes = form.minutes.data
    seconds = form.seconds.data
    ending_time = time(hour=0, minute=minutes + (round - 1) * 5, second=seconds)
    return ending_time

