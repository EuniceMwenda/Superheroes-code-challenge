#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Hero

import os

from flask import Flask, jsonify, request, abort
from models import db, Hero, Power, HeroPower

db_path = os.path.join(os.path.dirname(__file__), 'db', 'app.db')


app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/app.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

# ... existing code ...

@app.route('/heroes', methods=['GET'])
def get_heroes():
    heroes = Hero.query.all()
    hero_list = [{'id': hero.id, 'name': hero.name, 'super_name': hero.super_name} for hero in heroes]
    return jsonify(hero_list)

@app.route('/heroes/<int:hero_id>', methods=['GET'])
def get_hero(hero_id):
    hero = Hero.query.get(hero_id)
    if hero is None:
        abort(404, {'error': 'Hero not found'})
    
    powers = [{'id': power.id, 'name': power.name, 'description': power.description} for power in hero.powers]
    hero_data = {
        'id': hero.id,
        'name': hero.name,
        'super_name': hero.super_name,
        'powers': powers
    }
    return jsonify(hero_data)

@app.route('/powers', methods=['GET'])
def get_powers():
    powers = Power.query.all()
    power_list = [{'id': power.id, 'name': power.name, 'description': power.description} for power in powers]
    return jsonify(power_list)

@app.route('/powers/<int:power_id>', methods=['GET'])
def get_power(power_id):
    power = Power.query.get(power_id)
    if power is None:
        abort(404, {'error': 'Power not found'})
    
    power_data = {
        'id': power.id,
        'name': power.name,
        'description': power.description
    }
    return jsonify(power_data)

@app.route('/powers/<int:power_id>', methods=['PATCH'])
def update_power(power_id):
    power = Power.query.get(power_id)
    if power is None:
        abort(404, {'error': 'Power not found'})
    
    data = request.get_json()
    if 'description' not in data:
        abort(400, {'error': 'Missing description in request body'})
    
    power.description = data['description']
    
    try:
        db.session.commit()
        return jsonify({'id': power.id, 'name': power.name, 'description': power.description})
    except Exception as e:
        db.session.rollback()
        abort(400, {'error': f'Failed to update power: {str(e)}'})

@app.route('/hero_powers', methods=['POST'])
def create_hero_power():
    data = request.get_json()
    if 'strength' not in data or 'power_id' not in data or 'hero_id' not in data:
        abort(400, {'error': 'Missing required parameters in request body'})
    
    hero = Hero.query.get(data['hero_id'])
    power = Power.query.get(data['power_id'])
    
    if hero is None or power is None:
        abort(404, {'error': 'Hero or Power not found'})
    
    hero_power = HeroPower(strength=data['strength'], hero=hero, power=power)
    
    try:
        db.session.add(hero_power)
        db.session.commit()
        return get_hero(hero.id)  # Return hero data after adding the power
    except Exception as e:
        db.session.rollback()
        abort(400, {'error': f'Failed to create HeroPower: {str(e)}'})

if __name__ == '__main__':
    app.run(port=5555)

