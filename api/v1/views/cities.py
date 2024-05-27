#!/usr/bin/python3
"""Implement city view"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<state_id>/cities', methods=['GET'])
def get_cities(state_id):
    """get a list of cities """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    cities = [obj.to_dict() for obj in state.cities]
    return make_response(jsonify(cities), 200)


@app_views.route('/cities/<city_id>', methods=['GET'])
def get_city(city_id):
    """get city by id"""
    city = storage.get(City, city_id)
    return make_response(jsonify(city.to_dict()),
                         200) if city else abort(404)


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    """delete city"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    city.delete()
    storage.save()
    return make_response({}, 200)


@app_views.route('states/<state_id>/cities', methods=['POST'])
def create_city(state_id):
    """create a new city"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    city = request.get_json()
    if not city:
        return make_response("Not a JSON", 400)
    if not city.get('name'):
        return make_response("Missing name", 400)
    city['state_id'] = state_id
    new_city = City(**city)
    new_city.save()
    return make_response(jsonify(new_city.to_dict()), 201)


@app_views.route('cities/<city_id>', methods=['PUT'])
def update_city(city_id):
    """update a city by id"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    req_city = request.get_json()
    if not req_city:
        return make_response("Not a JSON", 400)
    setattr(city, 'name', req_city.get('name'))
    storage.save()
    return make_response(city.to_dict(), 200)
