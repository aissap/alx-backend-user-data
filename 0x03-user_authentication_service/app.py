#!/usr/bin/env python3
"""
Basic Flask app
"""
from flask import Flask, jsonify
from auth import Auth


app = Flask(__name__)
AUTH = Auth()


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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
