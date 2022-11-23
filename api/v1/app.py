#!/usr/bin/python3
""" Flask Application """
import os
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def close_storage(error):
    """close all storage"""
    storage.close()


@app.errorhandler(404)
def invalid_route(error):
    return jsonify({"error": "Not found"})


if __name__ == "__main__":
    """Main function"""
    host = os.environ.get('HBNB_API_HOST')
    port = os.environ.get('HBNB_API_PORT')

    if not host:
        host = '0.0.0.0'
    if not port:
        port = '5000'

    app.run(host=host, port=port, threaded=True)
