#!/usr/bin/python3
"""
Module for methods used by app_view blueprint
"""
from api.v1.views import app_views
from flask import jsonify, make_response, request, abort
from models import storage
from models.state import State
from flasgger import swag_from


@app_views.route('/states', methods=['GET'], strict_slashes=False)
@swag_from('swagger_spec/get_states.yml')
def get_states():
    """Retrieves the list of all State objects"""
    state_list = list(storage.all(State).values())
    state_dict = [state.to_dict() for state in state_list]
    return jsonify(state_dict)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
@swag_from('swagger_spec/get_state.yml')
def get_state(state_id):
    """Retrieves a State object"""
    state_obj = storage.get(State, state_id)
    if state_obj is None:
        abort(404)
    return jsonify(state_obj.to_dict())


@app_views.route('/states', methods=['POST'], strict_slashes=False)
@swag_from('swagger_spec/create_state.yml')
def create_state():
    """Creates a new State object"""
    data = request.get_json()
    if type(data) is not dict:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'name' not in data:
        return make_response(jsonify({'error': 'Missing name'}), 400)
    new_obj = State()
    for key, value in data.items():
        if key != 'id' and key != 'created_at' and key != 'updated_at':
            setattr(new_obj, key, value)
    new_obj.save()
    return make_response(jsonify(new_obj.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
@swag_from('swagger_spec/delete_state.yml')
def delete_state(state_id):
    """Deletes a State object"""
    state_obj = storage.get(State, state_id)
    if state_obj is None:
        abort(404)
    state_obj.delete()
    storage.save()
    return jsonify({})


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
@swag_from('swagger_spec/update_state.yml')
def update_state(state_id):
    """Updates a State object"""
    state_obj = storage.get(State, state_id)
    if state_obj is None:
        abort(404)
    data = request.get_json()
    if type(data) is not dict:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for key, value in data.items():
        if key != 'id' and key != 'created_at' and key != 'updated_at':
            setattr(state_obj, key, value)
    state_obj.save()
    return jsonify(state_obj.to_dict())
