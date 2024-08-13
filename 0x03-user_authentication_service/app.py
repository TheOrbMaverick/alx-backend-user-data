#!/usr/bin/env python3
"""
Basic Flask app
"""
from flask import Flask, jsonify, request
from auth import Auth


app = Flask(__name__)

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
        user = Auth.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400





if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
