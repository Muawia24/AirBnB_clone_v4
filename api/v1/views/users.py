#!/usr/bin/python3
"""
view for User objects that handles all default RESTFul API actions
"""
from models import storage
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.user import User
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response


@app_views.route('/users', methods=['GET'],
                 strict_slashes=False)
def all_users():
    """Retrieves the list of all User objects """
    users = storage.all(User).values()
    users_list = []
    for user in users:
        users_list.append(user.to_dict())
    return jsonify(users_list)


@app_views.route('/users/<user_id>', methods=['GET'],
                 strict_slashes=False)
def get_user(user_id):
    """Retrieves a User object by id """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """Deletes a User object"""
    user_delete = storage.get(User, user_id)
    if not user_delete:
        abort(404)
    storage.delete(user_delete)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/users', methods=['POST'],
                 strict_slashes=False)
def post_user():
    """Creates a User """
    json_data = request.get_json()
    if not json_data:
        abort(400, description="Not a JSON")
    if 'email' not in json_data:
        abort(400, description="Missing email")
    if 'password' not in json_data:
        abort(400, description="Missing password")

    new_user = User(**json_data)
    new_user.save()
    return make_response(jsonify(new_user.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
def update_user(user_id):
    """Updates a Amenity objec """
    user_update = storage.get(User, user_id)
    if not user_update:
        abort(404)

    json_data = request.get_json()
    if not json_data:
        abort(400, description="Not a JSON")
    ignore = ['id', 'email', 'created_at', 'updated_at']
    for key, value in json_data.items():
        if key not in ignore:
            setattr(user_update, key, value)
    storage.save()
    return make_response(jsonify(user_update.to_dict()), 200)
