#!/usr/bin/python3
"""Implement places_amenities view"""

from flask import abort, jsonify

from api.v1.views import app_views
from models import storage
from models.place import Place
from models.amenity import Amenity
from os import getenv


@app_views.route('/places/<place_id>/amenities', methods=['GET'])
def get_amenities_by_place_id(place_id):
    """Get amenities by place id"""
    place_by_id = storage.get(Place, place_id)

    if not place_by_id:
        abort(404)

    amenities_list = [amenity.to_dict() for amenity in place_by_id.amenities]

    return jsonify(amenities_list), 200


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'])
def delete_amenties(place_id, amenity_id):
    """Deletes a Amenity object to a Place"""
    place_by_id = storage.get(Place, place_id)
    if not place_by_id:
        abort(404)

    amenity_by_id = storage.get(Amenity, amenity_id)
    if not amenity_by_id:
        abort(404)

    if getenv('HBNB_TYPE_STORAGE') == 'db':
        amenities_by_place = place_by_id.amenities
    else:
        amenities_by_place = place_by_id.amenity_ids

    if amenity_by_id not in amenities_by_place:
        abort(404)

    amenities_by_place.remove(amenity_by_id)
    place_by_id.save()

    return jsonify({}), 200


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['POST'])
def link_amenity_to_place(place_id, amenity_id):
    """Link a Amenity object to a Place"""
    place_by_id = storage.get(Place, place_id)
    if not place_by_id:
        abort(404)

    amenity_by_id = storage.get(Amenity, amenity_id)
    if not amenity_by_id:
        abort(404)

    if getenv('HBNB_TYPE_STORAGE') == 'db':
        amenities_by_place = place_by_id.amenities
    else:
        amenities_by_place = place_by_id.amenity_ids

    if amenity_by_id in amenities_by_place:
        return jsonify(amenity_by_id.to_dict()), 200

    amenities_by_place.append(amenity_by_id.to_dict())
    place_by_id.save()

    return jsonify(amenity_by_id), 201
