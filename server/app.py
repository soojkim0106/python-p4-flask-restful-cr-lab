#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = True

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

class Plants(Resource):
    
    def get(self):
        
        plant_dict_list = [n.to_dict() for n in Plant.query.all()]
        
        return plant_dict_list, 200
    
    def post(self):
        
        data = request.json
        
        new_plant = Plant(
            name = data.get("name"),
            price = data.get("price"),
            image = data.get("image"),
            
        )
        
        db.session.add(new_plant)
        db.session.commit()
        
        plant_dict = new_plant.to_dict()
        
        return plant_dict, 201
    
api.add_resource(Plants, '/plants')

class PlantByID(Resource):
    
    def get(self, id):
        plant_dict = db.session.get(Plant, id).to_dict()

        return plant_dict, 200
    
api.add_resource(PlantByID, '/plants/<int:id>')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
