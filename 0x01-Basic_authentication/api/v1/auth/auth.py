#!/usr/bin/env python3
"""Class that manages the user authentication"""
from flask import request
from typing import List, TypeVar


class Auth:
    """authentication class handler"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Identifies the paths that are to be excluded"""
        return False

    def authorization_header(self, request=None) -> str:
        """Returns None at the moment"""
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Returns None at the moment"""
        return None
