#!/usr/bin/python3
"""Implement places view"""
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.city import City
from models.place import Place
from models.user import User
from models.state import State
from models.amenity import Amenity
from os import getenv


@app_views.route('/cities/<city_id>/places', methods=['GET'])
def get_places(city_id):
    """Get all places by specific city id."""
    city_by_id = storage.get(City, city_id)
    if not city_by_id:
        abort(404)

    place_list = [place.to_dict() for place in city_by_id.places]
    return make_response(jsonify(place_list), 200)


@app_views.route('/places/<place_id>', methods=['GET'])
def get_places_by_id(place_id):
    """Return place based on a corresponding id"""
    places_by_id = storage.get(Place, place_id)
    if not places_by_id:
        abort(404)

    return make_response(jsonify(places_by_id.to_dict()), 200)


@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    """Deletes a place with specific id"""
    place_by_id = storage.get(Place, place_id)
    if not place_by_id:
        abort(404)

    place_by_id.delete()
    storage.save()

    return make_response({}, 200)


@app_views.route('/cities/<city_id>/places', methods=['POST'])
def create_place(city_id):
    """Creates new place"""
    city_by_id = storage.get(City, city_id)
    if not city_by_id:
        abort(404)

    body_request = request.get_json()
    if not body_request:
        return make_response("Not a JSON", 400)
    if not body_request.get("user_id"):
        return make_response("Missing user_id", 400)
    if not body_request.get("name"):
        return make_response("Missing name", 400)

    user_by_id = storage.get(User, body_request.get('user_id'))
    if not user_by_id:
        abort(404)

    body_request["city_id"] = city_id
    place = Place(**body_request)
    place.save()

    return make_response(jsonify(place.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'])
def update_place(place_id):
    """Updates a place with specific id"""
    place_by_id = storage.get(Place, place_id)
    if not place_by_id:
        abort(404)

    body_request = request.get_json()
    if not body_request:
        return make_response("Not a JSON", 400)

    attributes_to_update = ['name', 'description', 'number_rooms',
                            'number_bathrooms', 'max_guest', 'price_by_night',
                            'latitude', 'longitude']

    for attribute in attributes_to_update:
        setattr(place_by_id, attribute,
                body_request.get(attribute, getattr(place_by_id, attribute)))
    storage.save()

    return make_response(jsonify(place_by_id.to_dict()), 200)


@app_views.route('/places_search', methods=['POST'])
def places_search():
    """retrieves all Place objects depending of the body of the request."""
    body_request = request.get_json()
    if body_request is None:
        abort(400, 'Not a JSON')

    states_ids = body_request.get('states', [])
    cities_ids = body_request.get('cities', [])
    amenities_ids = body_request.get('amenities')

    if len(body_request) == 0 or (len(states_ids) == 0 and
                                  len(cities_ids) == 0 and
                                  not amenities_ids):
        return jsonify([place.to_dict()
                        for place in storage.all('Place').values()])

    if len(states_ids) == 0 and len(cities_ids) == 0:
        places_list = storage.all(Place).values()
    else:
        places_list = []

    cities_by_states = []

    for state_id in states_ids:
        state = storage.get(State, state_id)
        if state:
            cities_by_state = state.cities
            cities_by_states.extend(cities_by_state)
            for city in cities_by_state:
                places_list.extend(city.places)

    cities_ids = body_request.get('cities', [])
    for city_id in cities_ids:
        city_by_id = storage.get(City, city_id)
        if city_by_id and city_by_id not in cities_by_states:
            places_list.extend(city_by_id.places)

    if amenities_ids:
        amenities_list = []
        for amenity_id in amenities_ids:
            amenity = storage.get(Amenity, amenity_id)
            if amenity:
                amenities_list.append(amenity)

        places_list = filter_places_with_amenities(places_list, amenities_list)

    return jsonify([place.to_dict() for place in places_list])


def filter_places_with_amenities(places, amenities):
    filtered_places = []
    for place in places:
        if getenv('HBNB_TYPE_STORAGE') == 'db':
            amenities_by_place = place.amenities
        else:
            amenities_by_place = place.amenity_ids
        for amenity in amenities_by_place:
            if amenity in amenities:
                filtered_places.append(place)
                break
    return filtered_places
