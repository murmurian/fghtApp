from db import db


def add_fight(fight_data):
    sql = "INSERT INTO fights (fighter1, fighter2, referee, rounds, ending_time, winner, winning_method, date, event, fight_order, weight_class, draw) VALUES (:fighter1, :fighter2, :referee, :rounds, :ending_time, :winner, :winning_method, :date, :event, :fight_order, :weight_class, :draw)"
    db.session.execute(sql, fight_data)
    db.session.commit()


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


