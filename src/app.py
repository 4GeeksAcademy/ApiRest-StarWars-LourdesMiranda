"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Character, Planet, Favourite
# from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace(
        "postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object


@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints


@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/users', methods=['GET'])
def get_users():

    users = User.query.all()
    response_body = [user.serialize() for user in users]

    return jsonify(response_body), 200


@app.route('/people', methods=['GET'])
def get_people():

    characters = Character.query.all()
    response_body = [character.serialize() for character in characters]

    return jsonify(response_body), 200

@app.route('/people/<int:people_id>', methods=['GET'])
def get_person(people_id):

    character = Character.query.get(people_id)
    response_body = character.serialize()
    
    return jsonify(response_body), 200

@app.route('/planets', methods=['GET'])
def get_planets():

    planets = Planet.query.all()
    response_body = [planet.serialize() for planet in planets]

    return jsonify(response_body), 200

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planetas(planet_id):
    planets = Planet.query.get(planet_id)
    response_body = planets.serialize()
    
    return jsonify(response_body), 200

@app.route('/users/favourites', methods=['GET'])
def get_user_favourites():
    user_id = 1 
    favourites = Favourite.query.filter_by(user_id=user_id).all()
    response_body = [favourite.serialize() for favourite in favourites]
    return jsonify(response_body), 200

@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):
    new_favourite = Favourite(user_id=1, planet_id=planet_id)
    db.session.add(new_favourite)
    db.session.commit()
    response_body = new_favourite.serialize()
    return jsonify(response_body), 201

@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_favorite_people(people_id):
    new_favourite = Favourite(user_id=1, character_id=people_id)
    db.session.add(new_favourite)
    db.session.commit()
    response_body = new_favourite.serialize()
    return jsonify(response_body), 201

@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
    favourite = Favourite.query.filter_by(user_id=1, planet_id=planet_id).first()
    db.session.delete(favourite)
    db.session.commit()
    response_body = favourite.serialize()
    return jsonify(response_body), 200

@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_favorite_people(people_id):
    favourite = Favourite.query.filter_by(user_id=1, character_id=people_id).first()
    db.session.delete(favourite)
    db.session.commit()
    response_body = favourite.serialize()
    return jsonify(response_body), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
