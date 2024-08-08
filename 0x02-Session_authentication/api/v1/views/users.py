#!/usr/bin/env python3
""" Module of Users views """
from flask import jsonify, abort, request
from api.v1.views import app_views
from models.user import User


@app_views.route('/api/v1/users',
                 methods=['GET'],
                 strict_slashes=False)
def get_users():
    """ GET /api/v1/users """
    users = User.all()
    users_list = [user.to_dict() for user in users]
    return jsonify(users_list)


@app_views.route('/api/v1/users/<user_id>',
                 methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """ GET /api/v1/users/<user_id> """
    if user_id == "me":
        if request.current_user is None:
            abort(404)
        return jsonify(request.current_user.to_dict())
    user = User.get(user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/api/v1/users',
                 methods=['POST'], strict_slashes=False)
def create_user():
    """ POST /api/v1/users """
    # Implementation here
    pass


@app_views.route('/api/v1/users/<user_id>',
                 methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """ PUT /api/v1/users/<user_id> """
    # Implementation here
    pass


@app_views.route('/api/v1/users/<user_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """ DELETE /api/v1/users/<user_id> """
    # Implementation here
    pass
