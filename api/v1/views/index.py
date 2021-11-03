#!/usr/bin/python3
"""
Module for methods used by app_view blueprint
"""
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from flasgger import swag_from


@app_views.route('/status')
@swag_from('swagger_spec/status.yml')
def status():
    """that returns a JSON: "status": 'OK'"""
    return jsonify({'status': 'OK'})


@app_views.route('/stats')
@swag_from('swagger_spec/stats.yml')
def stats():
    """returns a JSON with the number of each objects by type"""
    return jsonify(
        {
            'amenities': storage.count(Amenity),
            'cities': storage.count(City),
            'places': storage.count(Place),
            'reviews': storage.count(Review),
            'states': storage.count(State),
            'users': storage.count(User)
        })
