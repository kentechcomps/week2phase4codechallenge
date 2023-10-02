#!/usr/bin/env python3

from flask import Flask, make_response , jsonify , request
from flask_migrate import Migrate
from flask_restful import Api ,Resource
from models import db, Hero , Power , Heropower , validatedescription , validatestrenght

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

@app.route('/powers/<int:id>', methods=['PATCH'])
def update_power(id):
    power = Power.query.get(id)

    if power is None:
        return jsonify({'error': 'Power not found'}), 404

    # Parse the request JSON data
    data = request.get_json()

    # Update the power's description if provided
    if 'description' in data:
        power.description = data['description']

    # Validate the updated power
    validation_errors = validatedescription(power)

    if validation_errors:
        return jsonify({'errors': validation_errors}), 400

    # Commit changes to the database
    db.session.commit()

    # Serialize the updated power into JSON
    updated_power_data = {
        'id': power.id,
        'name': power.name,
        'description': power.description
    }

    return jsonify(updated_power_data) , 200

@app.route('/hero_powers', methods=['POST'])
def create_hero_power():
    # Parse the request JSON data
    data = request.get_json()

    # Create a new HeroPower instance
    hero_power = Heropower(
        hero_id=data.get('hero_id'),
        power_id=data.get('power_id'),
        strength=data.get('strength')
    )

      # Validate the HeroPower instance
    validation_errors = validatestrenght(hero_power)

    if validation_errors:
        return jsonify({'errors': validation_errors}), 400
    
    db.session.add(hero_power)
    db.session.commit()

    hero = Hero.query.get(hero_power.hero_id)

    if hero is None:
        return jsonify({'error': 'Hero not found'}), 404
     
    hero_data = {
        'id': hero.id,
        'name': hero.name,
        'super_name': hero.super_name,
        'powers': [
            {
                'id': power.id,
                'name': power.name,
                'description': power.description
            }
            for power in hero.hero_powers
        ]
    }

    return jsonify(hero_data) , 201

if __name__ == '__main__':
    app.run(port=5555)
