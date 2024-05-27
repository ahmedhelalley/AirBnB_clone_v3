#!/usr/bin/python3
"""states route"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'])
def get_states():
    """get a list of states"""
    states = [obj.to_dict() for obj in storage.all(State).values()]
    return make_response(jsonify(states), 200)


@app_views.route('/states/<state_id>', methods=['GET'])
def get_state_by_id(state_id):
    """get state by id"""
    state = storage.get(State, state_id)
    return make_response(jsonify(state.to_dict()),
                         200) if state else abort(404)


@app_views.route('/states', methods=['POST'])
def create_state():
    """create a new state"""
    state = request.get_json()
    if not state:
        return make_response("Not a JSON", 400)
    if not state.get('name'):
        return make_response("Missing name", 400)
    new_state = State(**state)
    new_state.save()
    return make_response(jsonify(new_state.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'])
def update_state(state_id):
    """update a state by id"""
    cur_state = storage.get(State, state_id)
    if not cur_state:
        abort(404)
    new_state = request.get_json()
    if not new_state:
        return make_response("Not a JSON", 400)
    setattr(cur_state, 'name', new_state.get('name'))
    storage.save()
    return make_response(cur_state.to_dict(), 200)


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    """delete state"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    state.delete()
    storage.save()
    return make_response({}, 200)
