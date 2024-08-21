#!/usr/bin/python3
"""
view for City objects that handles all default RESTFul API actions
"""
from models import storage
from models.state import State
from models.state import City
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def all_cities(state_id):
    """Retrieves the list of all State objects """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    cities_list = []
    for city in state.cities:
        cities_list.append(city.to_dict())
    return jsonify(cities_list)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """Retrieves a City object by id """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """Deletes a City object"""
    city_delete = storage.get(City, city_id)
    if not city_delete:
        abort(404)
    storage.delete(city_delete)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def post_city(state_id):
    """Creates a City """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    json_data = request.get_json()
    if not json_data:
        abort(400, description="Not a JSON")
    if 'name' not in json_data:
        abort(400, description="Missing name")

    new_city = City(**json_data)
    new_city.state_id = state.id
    new_city.save()
    return make_response(jsonify(new_city.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """Updates a City objec """
    city_update = storage.get(City, city_id)
    if not city_update:
        abort(404)

    json_data = request.get_json()
    if not json_data:
        abort(400, description="Not a JSON")
    ignore = ['id', 'state_id', 'created_at', 'updated_at']
    for key, value in json_data.items():
        if key not in ignore:
            setattr(city_update, key, value)
    storage.save()
    return make_response(jsonify(city_update.to_dict()), 200)
