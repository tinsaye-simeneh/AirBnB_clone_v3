#!/usr/bin/python3
"""
Module for methods used by app_view blueprint with Place class
"""
from api.v1.views import app_views
from flask import jsonify, make_response, request, abort
from models import storage
from models.city import City
from models.place import Place
from models.review import Review
from models.user import User
from flasgger import swag_from


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
@swag_from('swagger_spec/get_reviews.yml')
def get_reviews_by_place(place_id):
    """Retrieves the list of all Review objects according to a Place"""
    place = get_object(Place, place_id)
    review_dict = [review.to_dict() for review in place.reviews]
    return jsonify(review_dict)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
@swag_from('swagger_spec/get_review.yml')
def get_review(review_id):
    """Retrieves a Review object"""
    review_obj = get_object(Review, review_id)
    return jsonify(review_obj.to_dict())


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
@swag_from('swagger_spec/create_review.yml')
def create_review_according_to_place(place_id):
    """Creates a new Review object according to a place"""
    data = request.get_json()
    place = get_object(Place, place_id)
    if type(data) is not dict:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'user_id' not in data:
        return make_response(jsonify({'error': 'Missing user_id'}), 400)
    user = get_object(User, data['user_id'])
    if 'text' not in data:
        return make_response(jsonify({'error': 'Missing text'}), 400)
    new_review_obj = Review()
    for key, value in data.items():
        if key != 'id' and key != 'created_at' and key != 'updated_at':
            setattr(new_review_obj, key, value)
    setattr(new_review_obj, 'place_id', place.id)
    new_review_obj.save()
    return make_response(jsonify(new_review_obj.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
@swag_from('swagger_spec/delete_review.yml')
def delete_review(review_id):
    """Deletes a Review object"""
    review_obj = get_object(Review, review_id)
    review_obj.delete()
    storage.save()
    return jsonify({})


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
@swag_from('swagger_spec/update_review.yml')
def update_review(review_id):
    """Updates a Review object"""
    review_obj = get_object(Review, review_id)
    data = request.get_json()
    if type(data) is not dict:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for key, value in data.items():
        if (key != 'id' and key != 'created_at' and key != 'updated_at' and
                key != 'user_id'):
            setattr(review_obj, key, value)
    review_obj.save()
    return jsonify(review_obj.to_dict())


def get_object(cls, obj_id):
    obj = storage.get(cls, obj_id)
    if obj is None:
        abort(404)
    return obj
