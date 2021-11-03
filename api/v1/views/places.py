#!/usr/bin/python3
"""
Module for methods used by app_view blueprint with Place class
"""
from api.v1.views import app_views
from flask import jsonify, make_response, request, abort
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.user import User
from models.state import State
from os import environ
from flasgger import swag_from


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
@swag_from('swagger_spec/get_places.yml')
def get_places_by_city(city_id):
    """Retrieves the list of all Place objects according to a City"""
    city = get_object(City, city_id)
    place_dict = [place.to_dict() for place in city.places]
    return jsonify(place_dict)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
@swag_from('swagger_spec/get_place.yml')
def get_place(place_id):
    """Retrieves a Place object"""
    place_obj = get_object(Place, place_id)
    return jsonify(place_obj.to_dict())


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
@swag_from('swagger_spec/create_place.yml')
def create_place_according_to_city(city_id):
    """Creates a new Place object according to a city"""
    data = request.get_json()
    city = get_object(City, city_id)
    if type(data) is not dict:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'user_id' not in data:
        return make_response(jsonify({'error': 'Missing user_id'}), 400)
    user = get_object(User, data['user_id'])
    if 'name' not in data:
        return make_response(jsonify({'error': 'Missing name'}), 400)
    new_place_obj = Place()
    for key, value in data.items():
        if key != 'id' and key != 'created_at' and key != 'updated_at':
            setattr(new_place_obj, key, value)
    setattr(new_place_obj, 'city_id', city.id)
    new_place_obj.save()
    return make_response(jsonify(new_place_obj.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
@swag_from('swagger_spec/delete_place.yml')
def delete_place(place_id):
    """Deletes a Place object"""
    place_obj = get_object(Place, place_id)
    place_obj.delete()
    storage.save()
    return jsonify({})


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
@swag_from('swagger_spec/update_place.yml')
def update_place(place_id):
    """Updates a Place object"""
    place_obj = get_object(Place, place_id)
    data = request.get_json()
    if type(data) is not dict:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for key, value in data.items():
        if (key != 'id' and key != 'created_at' and key != 'updated_at' and
                key != 'user_id'):
            setattr(place_obj, key, value)
    place_obj.save()
    return jsonify(place_obj.to_dict())


@app_views.route('/places_search', methods=['POST'],
                 strict_slashes=False)
@swag_from('swagger_spec/search_places.yml')
def search_places():
    """Searches Places to data"""
    data = request.get_json()
    if type(data) is not dict:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if len(data) == 0:
        list_places = [place.to_dict()
                       for place in storage.all(Place).values()]
        return jsonify(list_places)
    len_states = len(data['states']) if 'states' in data else 0
    len_cities = len(data['cities']) if 'cities' in data else 0
    len_amenities = len(data['amenities']) if 'amenities' in data else 0
    if len_states == 0 and len_cities == 0 and len_amenities == 0:
        list_places = [place.to_dict()
                       for place in storage.all(Place).values()]
        return jsonify(list_places)
    list_states = []
    list_cities = []
    if len_states > 0:
        for state_id in data['states']:
            list_states.append(get_object(State, state_id))
        for state in list_states:
            for city in state.cities:
                list_cities.append(city)
    if len_cities > 0:
        for city_id in data['cities']:
            list_cities.append(get_object(City, city_id))
    # print("this is list cities--------->>\n")
    # print(list_cities)
    list_cities = list(set(list_cities))
    list_places = []
    for city in list_cities:
        for place in city.places:
            list_places.append(place)
    if len_states == 0 and len_cities == 0:
        list_places = storage.all(Place).values()
    if (len_states > 0 or len_cities > 0) and len(list_places) == 0:
        return jsonify({})
    if len_amenities == 0:
        result = [place.to_dict() for place in list_places]
        return jsonify(result)
    places_in_search = []

    for place in list_places:
        checked = True
        if environ.get('HBNB_TYPE_STORAGE') == 'db':
            place_amenities = [amenity.id for amenity in place.amenities]
        else:
            place_amenities = place.amenity_ids
        for amenity_id in data['amenities']:
            if amenity_id not in place_amenities:
                checked = False
                break
        if checked is True:
            del(place.amenities)
            places_in_search.append(get_object(Place, place.id))
    result = [place.to_dict() for place in places_in_search]
    return jsonify(result)


def get_object(cls, obj_id):
    obj = storage.get(cls, obj_id)
    if obj is None:
        abort(404)
    return obj
