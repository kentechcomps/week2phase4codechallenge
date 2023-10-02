#!/usr/bin/env python3

from flask import Flask, make_response , jsonify
from flask_migrate import Migrate

from models import db, Hero

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return make_response(
        {'message': 'Karibu'},
        200
    )
@app.route('/heros' , methods = ['GET'])
def get_heroes():
    heros = Hero.query.all()
    herolist = []
     
    for hero in heros:
        herodata = hero.to_dict()
        herolist.append(herodata)

    return jsonify(herolist)

if __name__ == '__main__':
    app.run(port=5555)
