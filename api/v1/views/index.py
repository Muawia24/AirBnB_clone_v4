#!/usr/bin/python3
"""index.py """

from flask import jsonify
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route('/status', methods=['GET'])
def status():
    """ Api status"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'])
def count_all():
    """An endpoint that retrieves the number of each objects by type"""
    objs_count = {}
    objs = {"amenities": Amenity, "cities": City, "places": Place,
            "reviews": Review, "states": State, "users": User}
    for key, value in objs.items():
        objs_count[key] = storage.count(value)

    return jsonify(objs_count)
