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
from models import db, User, Planet
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity, create_access_token
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = "4geeks"  # Change this!
jwt = JWTManager(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

@app.route('/planet', methods=['GET'])
@jwt_required()
def getPlanets():
    planets = Planet.getAll()
    return jsonify(planets), 200

@app.route('/planet/<int:id>', methods=['GET'])
@jwt_required()
def getPlanet(id):
    planet = Planet.getPlanet(id)
 
@app.route('/planet/<int:id>', methods=['DELETE'])
@jwt_required()
def deletePlanet(id):
    planet = Planet.deletePlanet(id)
    return jsonify(planet), 200
    

@app.route('/login', methods=['POST'])
def sign_in():
    body = request.get_json()
    if body is None:
        return jsonify({"msg": "Body is empty"})
    
    email = body["email"]
    password = body["password"]

    user = User.getUser(email, password)
    if user is None:
        return jsonify({"msg": "Email or password incorrect"})
    
    token = create_access_token(identity=user.id)
    return jsonify({"token": token}), 200

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
