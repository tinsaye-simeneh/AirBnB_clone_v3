#!/usr/bin/python3
"""
Module for methods used by app_view blueprint with place_amenities relationship
"""
from api.v1.views import app_views
from flask import jsonify, make_response, request, abort
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.user import User
from os import environ
from flasgger import swag_from


@app_views.route('/places/<place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
@swag_from('swagger_spec/get_amenities_by_place.yml')
def get_amenities_by_place(place_id):
    """Retrieves the list of all Amenity objects according to a Place"""
    place = get_object(Place, place_id)
    amenity_dict = [amenity.to_dict() for amenity in place.amenities]
    return jsonify(amenity_dict)


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['POST'],
                 strict_slashes=False)
@swag_from('swagger_spec/link_amenity.yml')
def link_amenity_to_place(place_id, amenity_id):
    """Links an Amenity object a place"""
    place_obj = get_object(Place, place_id)
    amenity_obj = get_object(Amenity, amenity_id)
    if environ.get('HBNB_TYPE_STORAGE') != 'db':
        if amenity_id in place_obj.amenity_ids:
            return jsonify(amenity_obj.to_dict())
        else:
            place_obj.amenity_ids.append(amenity_id)
    else:
        if amenity_obj in place_obj.amenities:
            return jsonify(amenity_obj.to_dict())
        else:
            place_obj.amenities.append(amenity_obj)
    place_obj.save()
    return make_response(jsonify(amenity_obj.to_dict()), 201)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
@swag_from('swagger_spec/delete_amenity_by_place.yml')
def delete_amenity_from_place(place_id, amenity_id):
    """Deletes a Amenity object to a place"""
    place_obj = get_object(Place, place_id)
    amenity_obj = get_object(Amenity, amenity_id)
    if environ.get('HBNB_TYPE_STORAGE') != 'db':
        if amenity_id not in place_obj.amenity_ids:
            abort(404)
        place_obj.amenity_ids.remove(amenity_id)
    else:
        if amenity_obj not in place_obj.amenities:
            abort(404)
        place_obj.amenities.remove(amenity_obj)
    place_obj.save()
    return jsonify({})


def get_object(cls, obj_id):
    obj = storage.get(cls, obj_id)
    if obj is None:
        abort(404)
    return obj
