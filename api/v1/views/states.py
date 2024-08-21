#!/usr/bin/python3
"""
view for State objects that handles all default RESTFul API actions
"""
from models import storage
from models.state import State
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def all_states():
    """Retrieves the list of all State objects """
    states = storage.all(State).values()
    states_list = []
    for state in states:
        states_list.append(state.to_dict())
    return jsonify(states_list)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """Retrieves a State object by id """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """Deletes a State object"""
    state_delete = storage.get(State, state_id)
    if not state_delete:
        abort(404)
    storage.delete(state_delete)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_state():
    """Creates a State """
    json_data = request.get_json()
    if json_data is None:
        abort(400, description="Not a JSON")
    if 'name' not in json_data:
        abort(400, description="Missing name")

    new_state = State(**json_data)
    new_state.save()
    return make_response(jsonify(new_state.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """Updates a State objec """
    state_update = storage.get(State, state_id)
    if not state_update:
        abort(404)

    json_data = request.get_json()
    if not request.get_json():
        abort(400, description="Not a JSON")
    ignore = ['id', 'created_at', 'updated_at']
    for key, value in json_data.items():
        if key not in ignore:
            setattr(state_update, key, value)
    storage.save()
    return make_response(jsonify(state_update.to_dict()), 200)
