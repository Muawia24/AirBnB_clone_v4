#!/usr/bin/python3
"""
view for Review objects that handles all default RESTFul API actions
"""
from models import storage
from models.state import State
from models.city import City
from models.place import Place
from models.user import User
from models.review import Review
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def all_reviews(place_id):
    """Retrieves the list of all Review objects """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    reviews_list = []
    for review in place.reviews:
        reviews_list.append(review.to_dict())
    return jsonify(reviews_list)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """Retrieves a Review object by id """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """Deletes a Review object"""
    review_delete = storage.get(Review, review_id)
    if not review_delete:
        abort(404)
    storage.delete(review_delete)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def post_review(place_id):
    """Creates a Review """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    json_data = request.get_json()
    if not json_data:
        abort(400, description="Not a JSON")
    if 'text' not in json_data:
        abort(400, description="Missing text")
    if 'user_id' not in json_data:
        abort(400, description="Missing user_id")
    if not storage.get(User, json_data['user_id']):
        abort(404)

    new_review = Review(**json_data)
    new_review.place_id = place.id
    new_review.save()
    return make_response(jsonify(new_review.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """Updates a Review object """
    review_update = storage.get(Review, review_id)
    if not review_update:
        abort(404)

    json_data = request.get_json()
    if not json_data:
        abort(400, description="Not a JSON")
    ignore = ['id', 'place_id', 'user_id', 'created_at', 'updated_at']
    for key, value in json_data.items():
        if key not in ignore:
            setattr(review_update, key, value)
    storage.save()
    return make_response(jsonify(review_update.to_dict()), 200)
