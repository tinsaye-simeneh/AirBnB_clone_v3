#!/usr/bin/python3
"""
Module for methods used by app_view blueprint
"""
from api.v1.views import app_views
from flask import jsonify, make_response, request, abort
from models import storage
from models.city import City
from models.state import State
from flasgger import swag_from


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
@swag_from('swagger_spec/get_cities.yml')
def get_cities_by_state(state_id):
    """Retrieves the list of all City objects from a given State"""
    state_list = list(storage.all(State).values())
    state = [state for state in state_list if state.id == state_id]
    if len(state) == 0:
        abort(404)
    cities = state[0].cities
    cities = [city.to_dict() for city in cities]
    return jsonify(cities)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
@swag_from('swagger_spec/get_city.yml')
def get_city(city_id):
    """Retrieves a City object"""
    city_obj = storage.get(City, city_id)
    if city_obj is None:
        abort(404)
    return jsonify(city_obj.to_dict())


@app_views.route('states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
@swag_from('swagger_spec/create_city.yml')
def create_city(state_id):
    """Creates a new State object"""
    data = request.get_json()
    if type(data) is not dict:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'name' not in data:
        return make_response(jsonify({'error': 'Missing name'}), 400)
    state_obj = storage.get(State, state_id)
    if state_obj is None:
        abort(404)
    new_obj = City()
    for key, value in data.items():
        if key != 'id' and key != 'created_at' and key != 'updated_at':
            setattr(new_obj, key, value)
    setattr(new_obj, 'state_id', state_id)
    new_obj.save()
    return make_response(jsonify(new_obj.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
@swag_from('swagger_spec/delete_city.yml')
def delete_city(city_id):
    """Deletes a City object"""
    city_obj = storage.get(City, city_id)
    if city_obj is None:
        abort(404)
    city_obj.delete()
    storage.save()
    return jsonify({})


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
@swag_from('swagger_spec/update_city.yml')
def update_city(city_id):
    """Updates a City object"""
    city_obj = storage.get(City, city_id)
    if city_obj is None:
        abort(404)
    data = request.get_json()
    if type(data) is not dict:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for key, value in data.items():
        if key != 'id' and key != 'created_at' and key != 'updated_at':
            setattr(city_obj, key, value)
    city_obj.save()
    return jsonify(city_obj.to_dict())
