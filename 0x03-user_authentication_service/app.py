#!/usr/bin/env python3
"""flask app"""
from auth import Auth
from flask import abort, Flask, jsonify, request, redirect

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


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout():
    """Handling logging out a user"""
    # check for valid sessions
    cookie = request.cookies.get('session_id')
    if cookie is None:
        abort(403)

    # get the user from the session_id
    user = AUTH.get_user_from_session_id(cookie)
    if user is None:
        abort(403)

    # if valid user DELETE session_id`o`
    AUTH.destroy_session(user.id)
    return redirect('/')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
