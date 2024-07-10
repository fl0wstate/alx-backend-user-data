#!/usr/bin/env python3
"""Class that manages the user authentication"""
from flask import request
from typing import List, TypeVar


class Auth:
    """authentication class handler"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Identifies the paths that are to be excluded"""
        if path is not None:
            if not path.endswith('/'):
                path += '/'
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
