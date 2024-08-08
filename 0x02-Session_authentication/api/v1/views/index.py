#!/usr/bin/env python3
""" Module of Index views
"""
from flask import jsonify, abort
from api.v1.views import app_views

@app_views.route('/status',
                 methods=['GET'], strict_slashes=False)
def status() -> str:
    """ GET /api/v1/status
    Return:
      - the status of the API
    """
    return jsonify({"status": "OK"})

@app_views.route('/stats/', strict_slashes=False)
def stats() -> str:
    """ GET /api/v1/stats
    Return:
      - the number of each objects
    """
    from models.user import User
    stats = {}
    stats['users'] = User.count()
    return jsonify(stats)

@app_views.route('/api/v1/unauthorized',
                 methods=['GET'], strict_slashes=False)
def unauthorized() -> str:
    """ Endpoint to trigger a 401 error
    """
    abort(401)

@app_views.route('/api/v1/forbidden',
                 methods=['GET'], strict_slashes=False)
def forbidden() -> str:
    """ Endpoint to trigger a 403 error
    """
    abort(403)

@app_views.route('/api/v1/auth_session/login/',
                 methods=['GET'], strict_slashes=False)
def auth_session_login() -> str:
    """ Dummy endpoint to test exclusion """
    return jsonify({"message": "Login page"}), 200
