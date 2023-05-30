#!/usr/bin/python3
""" users places 
"""
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from api.v1.views import app_views


@app_views.route("/cities/<city_id>/places", methods=["GET"], strict_slashes=False)
def get_places_by_city(city_id):
    """Retrieve all Place objects of a City"""
    city = storage.get("City", city_id)
    if not city:
        abort(404)
    places_list = [place.to_dict() for place in city.places]
    return jsonify(places_list), 200


@app_views.route("/places/<place_id>", methods=["GET"], strict_slashes=False)
def get_place(place_id):
    """Retrieve a Place object by ID"""
    place = storage.get("Place", place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict()), 200


@app_views.route("/places/<place_id>", methods=["DELETE"], strict_slashes=False)
def delete_place(place_id):
    """Delete a Place object"""
    place = storage.get("Place", place_id)
    if not place:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route("/cities/<city_id>/places", methods=["POST"], strict_slashes=False)
def create_place(city_id):
    """Create a new Place"""
    city = storage.get("City", city_id)
    if not city:
        abort(404)
    params_json = request.get_json()
    if not params_json:
        abort(400, "Not a JSON")
    if "user_id" not in params_json:
        abort(400, "Missing user_id")
    if "name" not in params_json:
        abort(400, "Missing name")
    user = storage.get("User", params_json["user_id"])
    if not user:
        abort(404)
    params_json["city_id"] = city_id
    new_place = Place(**params_json)
    new_place.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route("/places/<place_id>", methods=["PUT"], strict_slashes=False)
def update_place(place_id):
    """Update a Place object"""
    place = storage.get("Place", place_id)
    if not place:
        abort(404)
    params_json = request.get_json()
    if not params_json:
        abort(400, "Not a JSON")
    ignore_keys = ["id", "user_id", "city_id", "created_at", "updated_at"]
    for key, value in params_json.items():
        if key not in ignore_keys:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict()), 200

