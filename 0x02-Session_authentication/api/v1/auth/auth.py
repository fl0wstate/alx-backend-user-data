#!/usr/bin/env python3
"""Class that manages the user authentication"""
from flask import request
from typing import List, TypeVar
from os import getenv
import fnmatch


class Auth:
    """authentication class handler"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Identifies the paths that are to be excluded"""
        if path is None:
            return True
        if excluded_paths is None:
            return True
        if len(excluded_paths) == 0:
            return True
        if not path.endswith('/'):
            path += '/'

        if path.find('*') >= 0:
            for pattern in excluded_paths:
                if not pattern.endswith('/') or not pattern.endswith('*'):
                    pattern += '/'
                if fnmatch.fnmatch(path, pattern):
                    return False
        else:
            if path in excluded_paths:
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """Grants access to the request
            if authorization_header is present
        """
        if request is None:
            return None
        if 'Authorization' not in request.headers:
            return None
        return request.headers['Authorization']

    def current_user(self, request=None) -> TypeVar('User'):
        """Returns None at the moment"""
        return None

    def session_cookie(self, request=None) -> str:
        """Returns a cookie value from a request made"""
        if request is None:
            return None
        try:
            cookie_dict = request.cookies
            return cookie_dict.get(getenv('SESSION_NAME'))
        except Exception:
            return None
