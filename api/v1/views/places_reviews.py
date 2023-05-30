#!/usr/bin/python3
""" places_reviews api v1 view """

from flask import jsonify, abort, request
from models import storage
from models.review import Review
from api.v1.views import app_views


@app_views.route("/places/<place_id>/reviews", methods=["GET"], strict_slashes=False)
def get_reviews(place_id):
    """Retrieve all Review objects of a Place"""
    place = storage.get("Place", place_id)
    if not place:
        abort(404)
    reviews_list = [review.to_dict() for review in place.reviews]
    return jsonify(reviews_list), 200


@app_views.route("/reviews/<review_id>", methods=["GET"], strict_slashes=False)
def get_review_id(review_id):
    """Retrieve a Review object by ID"""
    review = storage.get("Review", review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict()), 200


@app_views.route("/reviews/<review_id>", methods=["DELETE"], strict_slashes=False)
def delete_review(review_id):
    """Delete a Review object"""
    review = storage.get("Review", review_id)
    if not review:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route("/places/<place_id>/reviews", methods=["POST"], strict_slashes=False)
def create_review(place_id):
    """Create a new Review"""
    place = storage.get("Place", place_id)
    if not place:
        abort(404)
    params_json = request.get_json()
    if not params_json:
        abort(400, "Not a JSON")
    if "user_id" not in params_json:
        abort(400, "Missing user_id")
    if "text" not in params_json:
        abort(400, "Missing text")
    user = storage.get("User", params_json["user_id"])
    if not user:
        abort(404)
    params_json["place_id"] = place_id
    new_review = Review(**params_json)
    new_review.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route("/reviews/<review_id>", methods=["PUT"], strict_slashes=False)
def update_review(review_id):
    """Update a Review object"""
    review = storage.get("Review", review_id)
    if not review:
        abort(404)
    params_json = request.get_json()
    if not params_json:
        abort(400, "Not a JSON")
    ignore_keys = ["id", "user_id", "place_id", "created_at", "updated_at"]
    for key, value in params_json.items():
        if key not in ignore_keys:
            setattr(review, key, value)
    review.save()
    return jsonify(review.to_dict()), 200

