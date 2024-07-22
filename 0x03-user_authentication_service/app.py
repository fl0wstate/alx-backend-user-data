#!/usr/bin/env python3
"""flask app"""
from jinja2 import StrictUndefined
from sqlalchemy.sql.operators import op
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


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile():
    """Gets you the user_data according to the session_id given"""
    if request.headers:
        cookie = request.headers.get('Cookie')
        if cookie:
            session_id = cookie.split('=')[1]
            user = AUTH.get_user_from_session_id(session_id)
            if user:
                return jsonify({'email': user.email}), 200
            else:
                abort(403)
        else:
            abort(403)
    else:
        abort(403)


@app.route(
    '/reset_password',
    methods=['POST'],
    strict_slashes=False
)
def get_reset_password_token():
    """generates a new token for the user
    to create an new password"""
    mail = request.form.get('email')
    if mail:
        try:
            reset_token = AUTH.get_reset_password_token(mail)
            return jsonify({
                "email": mail,
                "reset_token": reset_token
            }), 200
        except Exception:
            abort(403)


@app.route('/reset_password', methods=['PUT'], strict_slashes=False)
def update_password():
    """endpoint for handling password reset for all the users
    currently requesting password reset"""
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_password = request.form.get('new_password')

    if not email or not reset_token or not new_password:
        abort(403)

    try:
        AUTH.update_password(reset_token, new_password)
        return jsonify({
            "email": email,
            "message": "Password updated"
        })
    except ValueError:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
