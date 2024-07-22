#!/usr/bin/env python3
"""flask app"""
from auth import Auth
from flask import Flask, jsonify, request, abort

AUTH = Auth()
app = Flask(__name__)


@app.route(
    '/',
    methods=['GET'],
    strict_slashes=False)
def root():
    """returns the root page for the flask app"""
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def users():
    """Handling users endpoint"""
    email = request.form.get('email')
    password = request.form.get('password')

    if not email or not password:
        abort(400)

    try:
        user = AUTH.register_user(email, password)
    except ValueError:
        # respond with something
        return jsonify({
            "message": "email already registered"
        }), 400

    return jsonify({
        "email": user.email,
        "message": "user created"
    }), 200


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login():
    """Handling longging in users"""
    email = request.form.get('email')
    pwd = request.form.get('password')

    if not AUTH.valid_login(email, pwd):
        abort(401)

    new_session_id = AUTH.create_session(email)
    captured_response = jsonify({
        "email": "user.email",
        "message": "logged in"
    })
    captured_response.set_cookie("session_id", new_session_id)
    return captured_response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
