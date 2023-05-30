#!/usr/bin/python3
"""
Starts the API server
"""
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
import os

app = Flask(__name__)
app.register_blueprint(app_views, url_prefix='/api/v1')

# Create CORS instance allowing /* for 0.0.0.0
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})

@app.errorhandler(404)
def not_found(error):
    """Handles 404 errors and returns a JSON response"""
    return jsonify({"error": "Not found"}), 404


@app.teardown_appcontext
def teardown_appcontext(exception):
    storage.close()


if __name__ == "__main__":
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = os.getenv('HBNB_API_PORT', '5000')
    app.run(host=host, port=port, threaded=True)

