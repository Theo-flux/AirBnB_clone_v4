#!/usr/bin/python3
""" State View """
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'])
@app_views.route('/state/<state_id>', methods=['GET'])
def get_states(state_id=None):
    """ Retrieves the list of all State objects or state by id """
    if state_id:
        state_by_id = storage.get(State, state_id)

        if not state_by_id:
            abort(404)
        else:
            return jsonify(state_by_id.to_dict())
    else:
        all_states = storage.all(State)
        state_list = []

        for state in all_states.values():
            state_list.append(state.to_dict())
        return jsonify(state_list)


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state_by_id(state_id=None):
    """ Deletes a State object by id """
    if state_id:
        to_be_deleted_state = storage.get(State, state_id)

        if to_be_deleted_state:
            delete_this_state = storage.delete(to_be_deleted_state)
            storage.save()
            return (jsonify({}), 200)
        else:
            abort(404)


@app_views.route('/states', methods=['POST'])
def create_state():
    """ Create a state obj """
    res = request.get_json()
    if (not res.json):
        abort(404, description="Not a JSON")

    if 'name' not in res.json:
        abort(404, description="Missing name")

    data = request.json
    instance = State(**data)
    instance.save()
    return (jsonify(instance.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'])
def update_state_by_id(state_id=None):
    """ Update an existing state obj """
    if not request.json:
        abort(400, description="Not a JSON")

    state = storage.get(State, state_id)

    if not state:
        abort(404)

    data = request.json
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)
    storage.save()
    return (jsonify(state.to_dict()), 200)
