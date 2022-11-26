#!/usr/bin/python3
""" Amenities views """
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from flask import abort, jsonify, request


@app_views.route("/amenities", methods=['GET'], strict_slashes=False)
@app_views.route("/amenities/<amenity_id>",
                 methods=['GET'], strict_slashes=False)
def get_amenity(amenity_id=None):
    """ Retrieves aan or list of all Amenity obj """
    if amenity_id:
        amenity_obj_by_id = storage.get(Amenity, amenity_id)

        if amenity_obj_by_id:
            return jsonify(amenity_obj_by_id.to_dict())
        else:
            abort(404)
    else:
        all_amenity_obj = storage.all(Amenity)
        amenity_list = []

        for amenity in all_amenity_obj.values():
            amenity_list.append(amenity.to_dict())

        return (jsonify(amenity_list), 200)


@app_views.route("/amenities/<amenity_id>",
                 methods=['DELETE'], strict_slashes=False)
def delete_amenity(amenity_id):
    """ Delete an Amenity Obj by id """
    amenity_to_be_deleted = storage.get(Amenity, amenity_id)
    if amenity_to_be_deleted:
        storage.delete(**amenity_to_be_deleted)
        storage.save()
        return (jsonify({}), 200)
    else:
        abort(404)


@app_views.route("/amenities", methods=['POST'], strict_slashes=False)
def create_amenity():
    """ Create a Amenity """
    if not request.json:
        abort(404, description="Not a JSON")

    if "name" not in request.json:
        abort(404, description="Missng name")

    data = request.json
    instance = Amenity(**data)
    instance.save()
    return (jsonify(instance.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>',
                 methods=['PUT'], strict_slashes=False)
def updat_amenity(amenity_id):
    """ Update an Amenity Obj """
    if not request.json:
        abort(400, description="Not a JSON")

    amenity = storage.get(Amenity, amenity_id)

    if not amenity:
        abort(404)

    data = request.json
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, key, value)
    storage.save()
    return (jsonify(amenity.to_dict()), 200)
