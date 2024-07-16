#!/usr/bin/env python3
"""
Route module for the API
"""
from api.v1.auth.auth import Auth
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
from os import getenv, write


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
auth = None
auth_type = getenv('AUTH_TYPE')

if auth_type:
    from api.v1.auth.auth import Auth
    from api.v1.auth.basic_auth import BasicAuth
    from api.v1.auth.session_auth import SessionAuth

    environ_auth_type = {
            "auth": Auth,
            "basic_auth": BasicAuth,
            "session_auth": SessionAuth
            }

    try:
        print(environ_auth_type[auth_type])
        auth = environ_auth_type[auth_type]()
    except Exception as e:
        write(1, b"Error finding environment variable :")


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized(error) -> str:
    """Unauthorized page access handler
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error) -> str:
    """Forbidden pages for the logged users
    """
    return jsonify({"error": "Forbidden"}), 403


@app.before_request
def before_request():
    """ Capturing all the request before making a 
    response to the client
    """
    if not auth:
        return
    auth_paths = [
            '/api/v1/status/',
            '/api/v1/unauthorized/',
            '/api/v1/forbidden/',
            '/api/v1/auth_session/login/'
            ]
    if not auth.require_auth(request.path, auth_paths):
        return
    if not auth.authorization_header(request): 
        abort(401)
    current_user = auth.current_user(request)
    if not current_user:
        abort(403)
    request.current_user = current_user


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
