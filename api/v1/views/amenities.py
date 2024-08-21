#!/usr/bin/python3
"""
view for Amenity objects that handles all default RESTFul API actions
"""
from models import storage
from models.state import State
from models.city import City
from models.amenity import Amenity
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response


@app_views.route('/amenities', methods=['GET'],
                 strict_slashes=False)
def all_amenities():
    """Retrieves the list of all Amenity objects """
    amenities = storage.all(Amenity).values()
    amenities_list = []
    for amenity in amenities:
        amenities_list.append(amenity.to_dict())
    return jsonify(amenities_list)


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenity(amenity_id):
    """Retrieves a Amenity object by id """
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """Deletes a Amenity object"""
    amenity_delete = storage.get(Amenity, amenity_id)
    if not amenity_delete:
        abort(404)
    storage.delete(amenity_delete)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/amenities', methods=['POST'],
                 strict_slashes=False)
def post_amenity():
    """Creates a Amenity """
    json_data = request.get_json()
    if not json_data:
        abort(400, description="Not a JSON")
    if 'name' not in json_data:
        abort(400, description="Missing name")

    new_amenity = Amenity(**json_data)
    new_amenity.save()
    return make_response(jsonify(new_amenity.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """Updates a Amenity objec """
    amenity_update = storage.get(Amenity, amenity_id)
    if not amenity_update:
        abort(404)

    json_data = request.get_json()
    if not json_data:
        abort(400, description="Not a JSON")
    ignore = ['id', 'created_at', 'updated_at']
    for key, value in json_data.items():
        if key not in ignore:
            setattr(amenity_update, key, value)
    storage.save()
    return make_response(jsonify(amenity_update.to_dict()), 200)
