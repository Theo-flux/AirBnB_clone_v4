#!/usr/bin/python3
""" Places views """
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.place import City
from models.user import User
from flask import jsonify, abort, request


@app_views.route("/places/<place_id>", methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """ Get Place Object """
    place = storage.get(Place, place_id)

    if place:
        return (jsonify(place.to_dict()), 200)
    else:
        abort(404)


@app_views.route("/cities/<city_id>/places",
                 methods=['GET'], strict_slashes=False)
def places_by_city_id(city_id):
    """ Get places related by city_id """
    all_places = storage.all(Place)
    places_list = []

    for place in all_places.value():
        if place.city_id == city_id:
            places_list.append(place.to_dict())

    if not places_list:
        abort(404)

    return jsonify(places_list)


@app_views.route("/places/<place_id>",
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    place_to_be_deleted = storage.get(Place, place_id)

    if not place_to_be_deleted:
        abort(404)

    storage.delete(place_to_be_deleted)
    storage.save()
    return (jsonify({}), 200)


@app_views.route("/cities/<city_id>/places",
                 methods=['POST'], strict_slashes=False)
def add_place(city_id):
    """ adds a place obj related by city_id """
    this_city = storage.get(City, city_id)

    if not this_city:
        abort(404)

    if not request_json:
        abort(404, description="Not a JSON")

    if "user_id" not in request_json:
        abort(404, description="Missing user_id")

    user = storage.get(User, user_id)

    if not user:
        abort(404)

    if "name" not in request.json:
        abort(404, description="Missing name")

    data = request.get_json()
    instance = Place(**data)
    instance.save()
    return (jsonify(instance.to_dict()), 201)


@app_views.route("places/<place_id>", methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """ update a place obj """
    place = storage.get(Place, place_id)

    if not place:
        abort(404)

    if not request.json:
        abort(404, description="Not a JSON")

    data = request.get_json()
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at', 'user_id', 'city_id']:
            setattr(place, key, value)
    storage.save()
    return (jsonify(place.to_dict()), 200)
