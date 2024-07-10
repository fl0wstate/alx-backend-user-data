#!/usr/bin/env python3
"""Basic authentication
class that inherits from Auth class"""

from .auth import Auth
from re import search


class BasicAuth(Auth):
    """Basic authentication class that inherits
        from Auth class"""
    def extract_base64_authorization_header(
            self,
            authorization_header: str
            ) -> str:
        """Generates a new authorization_header value
        to be used in the Authorization header"""
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if 'Basic' in authorization_header:
            if authorization_header.startswith('Basic'):
                sub = search('Basic', authorization_header)
                last_idx = sub.end()
                if authorization_header[last_idx] == " ":
                    return authorization_header[last_idx + 1:]
