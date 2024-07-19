#!/usr/bin/env python3
"""flask app"""
from flask import Flask, jsonify, request, abort
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


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
    if request.form:
        email = request.form.get('email')
        password = request.form.get('password')

        try:
            user = AUTH.register_user(email, password)
            return jsonify({
                "email": f"{user.email}",
                "message": "user created"
            })
        except ValueError:
            # respond with something
            return jsonify({
                "message": "email already registered"
            }), 400


@app.route('/login', methods=['POST'], strict_slashes=False)
def login():
    """Handling longging in users"""
    if request.form:
        email = request.form.get('email')
        pwd = request.form.get('password')

        if AUTH.valid_login(email, pwd):
            abort(401)

        # create the session id
        new_session_id = AUTH.create_session(email)
        captured_response =  jsonify({
            "email": "user.email",
            "message": "logged in"
        })
        captured_response.set_cookie("session_id", new_session_id)
        return captured_response
    else:
        return


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
