#!/usr/bin/python3
"""Implement different routes"""

from api.v1.views import app_views
from flask import jsonify
from models import storage

from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route('/status')
def status():
    """Return status: ok"""
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def count_objs():
    """Return json that have objects and their counts"""
    objs = {
        "amenities": Amenity,
        "cities": City,
        "places": Place,
        "reviews": Review,
        "states": State,
        "users": User
        }

    count_objs = {
      key: storage.count(value) for key, value in objs.items()
    }

    return jsonify(count_objs)
