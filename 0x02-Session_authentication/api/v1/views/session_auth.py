#!/usr/bin/env python3
"""Creating a session view page"""

from flask import jsonify, request
from api.v1.views import app_views
from os import getenv


@app_views.route(
        '/auth_session/login/',
        methods=['POST'],
        strict_slashes=False
    )
def session_handler():
    """returning the session id"""
    print('here')
    if request.method == 'POST':
        print('here')
        email_ = request.form.get('email')
        print('here')
        passwd_ = request.form.get('password')
        print('here')
        if email_ is None:
            return jsonify({ "error": "email missing" }), 400
        if passwd_ is None:
            return jsonify({ "error": "password missing" }), 400
        try:
            from models.user import User

            found_users = User.search({'email': email_})
            if found_users is None:
                return jsonify(
                        { "error": "no user found for this email" }
                        ), 404
            for user in found_users:
                if user.is_valid_password(passwd_):
                    from api.v1.app import auth

                    print(user)
                    user = user.to_json()
                    print(user)
                    session_id = auth.create_session(user.id)
                    print(session_id)
                    captured_response = jsonify(user)
                    captured_response.set_cookie(
                            getenv('SESSION_NAME'),
                            session_id
                            )
                    return captured_response

                else:
                    return jsonify({ "error": "wrong password" }), 401
        except Exception:
            return None
