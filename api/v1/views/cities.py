#!/usr/bin/python3
""" City views """
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State


@app_views.route("/states/<state_id>/cities",
                 methods=['GET'], strict_slashes=False)
def get_cities_by_state_id(state_id):
    """ Retrieves the list of all City objects of a State """
    all_city = storage.all(City)
    city_list = []

    for city in all_city.values():
        if city.state_id == state_id:
            city_list.append(city.to_dict())

    if city_list:
        return jsonify(city_list)
    else:
        return abort(404)


@app_views.route("/cities/<city_id>", methods=['GET'], strict_slashes=False)
def get_cities_by_city_id(city_id):
    """ Retrieves a City object """
    city_by_id = storage.get(City, city_id)

    if city_by_id:
        return jsonify(city_by_id.to_dict())


@app_views.route("/states/<state_id>/cities",
                 methods=['POST'], strict_slashes=False)
def create_city(state_id):
    """ Creates a city """
    if not storage.get(State, state_id):
        abort(404)

    if not request.json:
        abort(404, description="Not a JSON")

    if 'name' not in request.json:
        abort(404, description="Missing name")

    data = request.json
    data["state_id"] = state_id
    instance = City(**data)
    instance.save()
    return (jsonify(instance.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def get_city_id(city_id):
    """ Get city by id """
    if not request.json:
        abort(400, description="Not a JSON")

    city = storage.get(City, city_id)

    if not city:
        abort(404)

    data = request.json
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at', 'state_id']:
            setattr(city, key, value)
    storage.save()
    return (jsonify(city.to_dict()), 200)


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city_by_id(city_id):
    """ Delete a city """
    city = storage.get(City, city_id)

    if city:
        storage.delete(city)
        storage.save()
        return (jsonify({}), 200)
    else:
        abort(404)
