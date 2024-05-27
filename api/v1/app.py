#!/usr/bin/python3
"""Entry point for API"""

from api.v1.views import app_views

from flask import Flask, make_response, jsonify
from models import storage
from os import getenv
from flask_cors import CORS

app = Flask(__name__)

app.url_map.strict_slashes = False

app.register_blueprint(app_views)
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.errorhandler(404)
def not_found(error):
    """Implement Not found page"""
    return make_response(jsonify({"error": "Not found"}), 404)


@app.teardown_appcontext
def terminate(exc):
    """Close SQLAlchemy session"""
    storage.close()


if __name__ == "__main__":
    app.run(host=getenv('HBNB_API_HOST', '0.0.0.0'),
            port=getenv('HBNB_API_PORT', 5000),
            threaded=True)
