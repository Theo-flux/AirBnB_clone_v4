#!/usr/bin/python3
""" Index view """
from api.v1.views import app_views


@app_views.route('/status')
def status():
    return {"status": "Ok"}
