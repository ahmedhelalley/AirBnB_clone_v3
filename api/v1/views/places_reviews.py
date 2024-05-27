#!/usr/bin/python3
"""Implement reviews view"""

from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.review import Review
from models.place import Place
from models.user import User


@app_views.route('/places/<place_id>/reviews', methods=['GET'])
def get_reviews_by_place_id(place_id):
    """Get all reviews from storage based on place id"""
    place_by_id = storage.get(Place, place_id)

    if not place_by_id:
        abort(404)

    reviews = [review.to_dict() for review in place_by_id.reviews]

    return jsonify(reviews), 200


@app_views.route('/reviews/<review_id>', methods=['GET'])
def get_review_by_id(review_id):
    """Get review by a specific id"""
    review_by_id = storage.get(Review, review_id)

    if not review_by_id:
        abort(404)

    return jsonify(review_by_id.to_dict()), 200


@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def delete_review(review_id):
    """Delete review based on an id"""
    review_by_id = storage.get(Review, review_id)

    if not review_by_id:
        abort(404)

    review_by_id.delete()
    storage.save()

    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'])
def create_review(place_id):
    """Create a new review"""
    place_by_id = storage.get(Place, place_id)

    if not place_by_id:
        abort(404)

    body_request = request.get_json()
    if not body_request:
        abort(400, "Not a JSON")

    if "user_id" not in body_request.keys():
        abort(400, "Missing user_id")

    users = storage.all(User)
    user_by_id = users.get('User.' + body_request['user_id'])
    if not user_by_id:
        abort(404)

    if "text" not in body_request.keys():
        abort(400, "Missing text")

    body_request["place_id"] = place_id
    review = Review(**body_request)
    review.save()

    return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'])
def update_review(review_id):
    """Update review based on an id"""
    review_by_id = storage.get(Review, review_id)

    if not review_by_id:
        abort(404)

    body_request = request.get_json()
    if not body_request:
        abort(400, "Not a JSON")

    review_by_id.text = body_request.get('text', review_by_id.text)
    storage.save()

    return jsonify(review_by_id.to_dict()), 200
