#!/usr/bin/python3
"""
Defines the routes for the v1 views
"""
from flask import jsonify
from api.v1.views import app_views

@app_views.route('/status', methods=['GET'], strict_slashes=False)
def get_status():
    """
    Retrieves the status of the API
    """
    return jsonify({"status": "OK"})

