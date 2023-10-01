from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Hero(db.Model):
    __tablename__ = 'hero'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))

    power = db.relationship('Heropower', backref='hero')

class Power(db.Model):
    __tablename__ = 'power'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))

    hero = db.relationship('Heropower', backref='power')

class Heropower(db.Model):
    __tablename__ = 'Heropower'

    id = db.Column(db.Integer, primary_key=True)
    hero_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'))
    power_id = db.Column(db.Integer, db.ForeignKey('pizza.id'))

