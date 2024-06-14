#!/usr/bin/env python3
"""
Basic Flask app
"""
from flask import Flask, jsonify, request, abort
from auth import Auth


app = Flask(__name__)
AUTH = Auth()


@app.route("/")
def welcome():
    """
    Route to return a welcome message in JSON format.
    """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"])
def register_user():
    """
    Endpoint to register a user.
    """
    try:
        email = request.form["email"]
        password = request.form["password"]

        user = AUTH.register_user(email, password)

        return jsonify({"email": user.email, "message": "user created"}), 200

    except ValueError as err:
        return jsonify({"message": str(err)}), 400


@app.route('/sessions', methods=['POST'])
def login():
    """Handles login requests"""
    email = request.form.get('email')
    password = request.form.get('password')

    if not email or not password:
        abort(401)

    if not AUTH.valid_login(email, password):
        abort(401)

    session_id = AUTH.create_session(email)
    if not session_id:
        abort(401)

    response = jsonify({"email": email, "message": "logged in"})
    response.set_cookie("session_id", session_id)
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
