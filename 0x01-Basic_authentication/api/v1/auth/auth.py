#!/usr/bin/env python3
"""Class that manages the user authentication"""
from flask import request
from typing import List, TypeVar
import fnmatch


class Auth:
    """authentication class handler"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Identifies the paths that are to be excluded"""
        if path is None:
            return True
        if excluded_paths is None:
            return True
        try:
            if path:
                if not path.endswith('/'):
                    path += '/'
            for pattern in excluded_paths:
                if not pattern.endswith('/') and not pattern.endswith('*'):
                    pattern += '/'
                if fnmatch.fnmatch(path, pattern):
                    return False
        except Exception:
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
