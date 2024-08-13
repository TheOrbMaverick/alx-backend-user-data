#!/usr/bin/env python3
"""
Basic Flask app
"""
from flask import Flask, jsonify, request, abort, make_response, redirect
from auth import Auth


app = Flask(__name__)
AUTH = Auth()

@app.route("/", methods=["GET"])
def welcome() -> str:
    """
    Return a JSON payload with a welcome message.
    """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"])
def register_user() -> str:
    """
    Register a new user with email and password.
    """
    email = request.form.get("email")
    password = request.form.get("password")

    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=["POST"])
def login():
    """
    POST /sessions
    Log in a user and create a session.
    """
    email = request.form.get("email")
    password = request.form.get("password")

    if not AUTH.valid_login(email, password):
        abort(401)

    session_id = AUTH.create_session(email)
    response = make_response(jsonify({"email": email, "message": "logged in"}))
    response.set_cookie("session_id", session_id)
    return response


@app.route("/sessions", methods=["DELETE"])
def logout():
    """
    DELETE /sessions
    Log out a user by destroying their session.
    """
    session_id = request.cookies.get("session_id")
    if not session_id:
        abort(403)

    user = AUTH.get_user_from_session_id(session_id)
    if not user:
        abort(403)

    AUTH.destroy_session(user.id)
    return redirect("/")


@app.route("/profile", methods=["GET"])
def profile():
    """
    GET /profile
    Return user profile if session ID is valid.
    """
    session_id = request.cookies.get("session_id")
    if not session_id:
        abort(403)
    
    user = AUTH.get_user_from_session_id(session_id)
    if not user:
        abort(403)
    
    return jsonify({"email": user.email})


@app.route('/reset_password', methods=['POST'])
def get_reset_password_token():
    """
    Respond to the POST /reset_password route.
    """
    email = request.form.get('email')
    if not email:
        return jsonify({"message": "Email required"}), 400
    try:
        reset_token = AUTH.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": reset_token}), 200
    except ValueError:
        return jsonify({"message": "Email not found"}), 403


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
