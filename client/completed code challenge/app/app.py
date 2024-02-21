from flask import Flask, jsonify, make_response, request
from models import db, Hero, Power, HeroPower
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)
db.init_app(app)

@app.route('/')
def index():
    return "<h1>SuperHeroes Database</h1>"

@app.route('/heroes', methods=['GET'])
def get_all_heroes():
    heroes = Hero.query.all()
    all_heroes = []
    for one_hero in heroes:
        the_hero = {
            'id': one_hero.id,
            'name': one_hero.name,
            'super_name': one_hero.super_name
        }
        all_heroes.append(the_hero)
    
    return make_response(jsonify(all_heroes), 200)

@app.route('/heroes/<int:id>', methods=['GET'])
def get_single_hero_by_id(id):
    single_hero = Hero.query.get(id)
    if single_hero:
        single_hero_info = {
            'id': single_hero.id,
            'name': single_hero.name,
            'super_name': single_hero.super_name,
            'powers': [{'id':single_power.id, 'name':single_hero.name, 'description':single_power.description} for single_power in single_hero.powers]
        }
        return make_response(jsonify(single_hero_info), 200)
    else:
        return make_response(jsonify({'error':'The hero ID you entered does not exist'}), 404)

@app.route('/powers', methods=['GET'])
def get_all_powers():
    powers = Power.query.all()
    all_powers = []
    for single_power in powers:
        the_power = {
            'id': single_power.id,
            'name': single_power.name,
            'description': single_power.description
        }
        all_powers.append(the_power)
        
    return make_response(jsonify(all_powers), 200)

@app.route('/powers/<int:id>', methods=['GET'])
def get_single_power_by_id(id):
    single_power = Power.query.get(id)
    if single_power:
        single_power_info = {
            'id': single_power.id,
            'name': single_power.name,
            'description': single_power.description
        }
        return make_response(jsonify(single_power_info), 200)
    else:
        return make_response(jsonify({'error': 'The power ID you entered does not exist'}), 404)

@app.route('/powers/<int:id>', methods=['PATCH'])
def update_single_power_by_id(id):
    single_power = Power.query.get(id)
    
    if not single_power:
        return make_response(jsonify({"error": "Power not found"}), 404)

    data = request.get_json()

    if 'description' not in data:
        return make_response(jsonify({"error": "validation errors"}), 400)
    
    if len(data['description']) < 20:
        return make_response(jsonify({"error": "validation errors"}), 400)
    
    single_power.description = data['description']
    db.session.commit()
    
    changed_power = {
        "id": single_power.id,
        "name": single_power.name,
        "description": single_power.description
    }
    
    return make_response(jsonify(changed_power), 200)


@app.route('/hero_powers', methods=['POST'])
def create_new_hero_power():
    data = request.get_json()
    
    strength = data['strength']
    power_id = data['power_id']
    hero_id = data['hero_id']
    
    if not strength:
        return make_response(jsonify({"errors": ["strength not provided"]}), 400)

    if strength not in ['Strong', 'Weak', 'Average']:
        return make_response(jsonify({"errors": ["Strength type is not accepted"]}), 400)
    
    check_hero = Hero.query.get(hero_id)
    check_power = Power.query.get(power_id)
    
    if not check_hero:
        return make_response(jsonify({"error": "Hero ID not found"}), 404)
    
    if not check_power:
        return make_response(jsonify({"error": "Power ID not found"}), 404)

    new_hero_power = HeroPower(strength=strength,hero=check_hero, power=check_power)
    db.session.add(new_hero_power)
    db.session.commit()
    
    info_about_hero = {
        'id': check_hero.id,
        'name': check_hero.name,
        'super_name': check_hero.super_name,
        'powers': [{'id': single_power.id, 'name':single_power.name, 'description':single_power.description} for single_power in check_hero.powers]
    }
    
    return make_response(jsonify(info_about_hero), 200)
    
if __name__ == '__main__':
    app.run(debug=True, port=5555)
