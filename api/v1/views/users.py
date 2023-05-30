#!/usr/bin/python3
"""users api views
"""
from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.user import User


@app_views.route("/users", methods=["GET"], strict_slashes=False)
def get_all_users():
    """Retrieve all users"""
    users = storage.all(User).values()
    users_list = [user.to_dict() for user in users]
    return jsonify(users_list), 200


@app_views.route("/users/<user_id>", methods=["GET"], strict_slashes=False)
def get_user(user_id):
    """Retrieve a user by ID"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict()), 200


@app_views.route("/users/<user_id>", methods=["DELETE"], strict_slashes=False)
def delete_user(user_id):
    """Delete a user"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route("/users", methods=["POST"], strict_slashes=False)
def create_user():
    """Create a new user"""
    params_json = request.get_json()
    if not params_json:
        abort(400, "Not a JSON")
    if "email" not in params_json:
        abort(400, "Missing email")
    if "password" not in params_json:
        abort(400, "Missing password")
    new_user = User(**params_json)
    new_user.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route("/users/<user_id>", methods=["PUT"], strict_slashes=False)
def update_user(user_id):
    """Update a user"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    params_json = request.get_json()
    if not params_json:
        abort(400, "Not a JSON")
    ignore_keys = ["id", "email", "created_at", "updated_at"]
    for key, value in params_json.items():
        if key not in ignore_keys:
            setattr(user, key, value)
    user.save()
    return jsonify(user.to_dict()), 200

