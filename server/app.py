#!/usr/bin/env python3

from flask import Flask, make_response , jsonify , request
from flask_migrate import Migrate
from flask_restful import Api ,Resource
from flask_cors import CORS
from models import db, Hero , Power , HeroPower

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

CORS(app)

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
        herodata ={
            "id" : hero.id ,
            "name" : hero.name ,
            "super_name" : hero.name
        }
        herolist.append(herodata)

    return jsonify(herolist)

class HeroByID(Resource):

    def get(self, id):

        responseobj= Hero.query.filter_by(id=id).first()
        response_dict = {
            "id" : responseobj.id ,
            "name" : responseobj.name ,
            "super_name" : responseobj.name

        }
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
        powerdata = {
          "id" : power.id ,
          "name" : power.name ,
          "description" : power.description  
        }
        powerlist.append(powerdata)

    return jsonify(powerlist)

class PowerByID(Resource):

    def get(self, id):

        response_dictobject = Power.query.filter_by(id=id).first()
        response_dict = {
            "id" : response_dictobject.id ,
            "name" : response_dictobject.name ,
            "description" : response_dictobject.description
        }
        if response_dict is None:
            return jsonify({'error': 'Power not found'}) , 404
        response = make_response(
            jsonify(response_dict),
            200,
        )

        return response

api.add_resource(PowerByID, '/powers/<int:id>')

@app.route('/powers/<int:id>', methods=['PATCH'])
def patch_power(id):
    try:

        power = Power.query.filter_by(id=id).first()
        print(power)

        if power:
            data = request.get_json()

            if 'description' in data:
                try:
                    description = data['description']
                    power.validate_description('description', description)
                except Exception as ve:
                    response_body = {"error":str(ve)}
                    return make_response(jsonify(response_body), 400)

            for key, value in data.items():
                setattr(power, key, value)

                db.session.add(power)
                db.session.commit()

                patched_power = {
                "id": power.id,
                "name": power.name,
                "description": power.description,
                }
                
                response = make_response(
                    jsonify(patched_power),
                    200
                )

            return response

        else:
            response_body = {"error":"Power Not Found"}
            return make_response(jsonify(response_body), 404)
    except Exception as e:
        app.logger.error(f"Error in PatchPower {str(e)}")
        return make_response({"error": "Serialization Error"}, 500)
    
@app.route('/hero_powers', methods=['POST'])
def post_hero_power(app):
    try:
        data = request.json

        if 'strength' in data:
            try:
                strength = data['strength']
                HeroPower.validate_strength(None, 'strength', strength)
            except Exception as ve:
                response_body = {"error": str(ve)}
                return make_response(jsonify(response_body), 400)

        hero = Hero.query.get(data.get('hero_id'))
        power = Power.query.get(data.get('power_id'))

        if not hero:
            response_body = {"error": "Hero with specified ID not found"}
            return make_response(jsonify(response_body), 404)

        if not power:
            response_body = {"error": "Power with the specified ID not found"}
            return make_response(jsonify(response_body), 404)

        new_hero_power = HeroPower(
            strength=data.get('strength'),
            hero_id=data.get('hero_id'),
            power_id=data.get('power_id')
        )

        db.session.add(new_hero_power)
        db.session.commit()

        created_HeroPowerdata = HeroPower.query.get(new_hero_power.id)
        
        response_body = {"message": "HeroPower created successfully", "data": created_HeroPower.to_dict()}
        return make_response(jsonify(response_body), 201)

    except Exception as e:
        app.logger.error(f"Error in post_hero_power: {str(e)}")
        response_body = {"error": "Serialization Error"}
        return make_response(jsonify(response_body), 500)

if __name__ == '__main__':
    app.run(port=5555)
