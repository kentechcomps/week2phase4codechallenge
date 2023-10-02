#!/usr/bin/env python3

from flask import Flask, make_response , jsonify
from flask_migrate import Migrate
from flask_restful import Api ,Resource
from models import db, Hero , Power

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

api =Api(app)
@app.route('/')
def index():
    return make_response(
        {'message': 'Karibu'},
        200
    )
@app.route('/heroes' , methods = ['GET'])
def get_heroes():
    heros = Hero.query.all()
    herolist = []
     
    for hero in heros:
        herodata = hero.to_dict()
        herolist.append(herodata)

    return jsonify(herolist)

class HeroByID(Resource):

    def get(self, id):

        response_dict = Hero.query.filter_by(id=id).first().to_dict()
        if response_dict is None:
            return jsonify({'error': 'Hero not found'}) , 404
        response = make_response(
            jsonify(response_dict),
            200,
        )

        return response

api.add_resource(HeroByID, '/heroes/<int:id>')


@app.route('/powers' , methods = ['GET'])
def get_powers():
    powers = Power.query.all()
    powerlist= []
     
    for power in powers:
        powerdata = power.to_dict()
        powerlist.append(powerdata)

    return jsonify(powerlist)

class PowerByID(Resource):

    def get(self, id):

        response_dict = Power.query.filter_by(id=id).first().to_dict()
        if response_dict is None:
            return jsonify({'error': 'Power not found'}) , 404
        response = make_response(
            jsonify(response_dict),
            200,
        )

        return response

api.add_resource(PowerByID, '/powers/<int:id>')

if __name__ == '__main__':
    app.run(port=5555)
