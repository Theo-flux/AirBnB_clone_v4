#!/usr/bin/python3
""" Users views """
from api.v1.views import app_views
from models.user import User
from models import storage
from flask import jsonify, abort, request


@app_views.route("/users", methods=['GET'], strict_slashes=False)
@app_views.route("/users/<user_id>", methods=['GET'], strict_slashes=False)
def get_user(user_id=None):
    """ Get user object(s) """
    if user_id:
        user = storage.get(User, user_id)

        if not user:
            abort(404)

        return jsonify(user.to_dict())
    else:
        all_users = storage.all(User)
        users_list = []

        for user in all_users.values():
            users_list.append(user.to_dict())

        return jsonify(users_list)


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user_by_id(user_id):
    """ Delete a user """
    user = storage.get(User, user_id)

    if user:
        storage.delete(user)
        storage.save()
        return (jsonify({}), 200)
    else:
        abort(404)


@app_views.route("/users",
                 methods=['POST'], strict_slashes=False)
def create_user():
    """ Creates a user """
    if not request.json:
        abort(404, description="Not a JSON")

    if 'name' not in request.json:
        abort(404, description="Missing name")

    data = request.get_json()
    instance = User(**data)
    instance.save()
    return (jsonify(instance.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user_by_id(user_id):
    """ Get city by id """
    if not request.json:
        abort(400, description="Not a JSON")

    user = storage.get(User, user_id)

    if not user:
        abort(404)

    data = request.get_json()
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at', 'email']:
            setattr(user, key, value)
    storage.save()
    return (jsonify(user.to_dict()), 200)
