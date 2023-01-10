from db import db
from flask import session

def add_fight(fight_data):
    sql = "INSERT INTO fights (fighter1, fighter2, referee, rounds, ending_time, winner, winning_method, date, event, fight_order, weight_class, draw) VALUES (:fighter1, :fighter2, :referee, :rounds, :ending_time, :winner, :winning_method, :date, :event, :fight_order, :weight_class, :draw)"
    db.session.execute(sql, fight_data)
    db.session.commit()