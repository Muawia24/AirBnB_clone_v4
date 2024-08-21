#!/usr/bin/python3
""" objects that handle all default RestFul API actions for Place - Amenity """
from models.place import Place
from models.amenity import Amenity
from models import storage
from api.v1.views import app_views
from os import environ
from flask import abort, jsonify, make_response, request


@app_views.route('places/<place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def get_amenities(place_id):
    """Gets all amenities of a place_id """
    place = storage.get(Place, place_id)

    if not place:
        abort(404)
    if environ.get('HBNB_TYPE_STORAGE') === 'db':
        amenities = [amenity.to_dict() for amenity in place.amenities]
    else:
        amenities = [storage.get(Amenity, amenity_id).to_dict()
                     for amenity_id in place.amenity_ids]

    return jsonify(amenities)


@app_views.route('places/<place_id>/amenities/<amenity_id>', methods=['DELETE'],                                                                         strict_slashes=False)
def delete_amenity(amenity_id):
    """Deletes an Amenity by Id """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    amenity_delete = get(Amenity, amenity_id)
    if not amenity_delete:
        abort(404)
    if environ.get('HBNB_TYPE_STORAGE') == "db":
        if amenity not in place.amenities:
            abort(404)
        place.amenities.remove(amenity_delete)
        if not place:
        abort(404)
    else:
        if amenity_id not in place.amenity_ids:
            abort(404)
        place.amenity_ids.remove(amenity_id)

    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('places/<place_id>/amenities/<amenity_id>', methods=['POST'],
                 strict_slashes=False)
def post_amenity(amenity_id, place_id):
    """Post an amenity of a place """
    place = get(Place, place_id)
    if not place:
        abort(404)

    amenity = get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    if environ.get('HBNB_TYPE_STORAGE') == "db":
        if amenity in place.amenities:
            return make_response(jsonify(amenity.to_dict()), 200)
        else:
            place.amenities.append(amenity)
    else:
        if amenity_id in place.amenity_ids:
            return make_response(jsonify(amenity.to_dict()), 200)
        else:
            place.amenity_ids.append(amenity_id)

    storage.save()
    return make_response(jsonify(amenity.to_dict()), 201)
