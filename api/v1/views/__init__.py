#!/usr/bin/python3
""" Blueprint for api """
from api.v1.views.index import *
from api.v1.views.states import *
from flask import Blueprint


app_views = Blueprint("app_views", __name__, url_prefix='/api/v1')
