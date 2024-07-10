#!/usr/bin/env python3
"""Basic authentication
class that inherits from Auth class"""

from .auth import Auth
from typing import TypeVar
from re import search
import base64


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

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """Checking for valid Base64encoding and decoding the data"""
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            decoded_data = base64.b64decode(
                    base64_authorization_header,
                    validate=True
                    )
            return decoded_data.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """the user email and password from the Base64 decoded value."""
        if decoded_base64_authorization_header is None:
            return None, None
        if not isinstance(
                decoded_base64_authorization_header,
                str):
            return None, None
        try:
            data = decoded_base64_authorization_header.split(':', 1)
            return data[0], data[1]
        except Exception:
            return None, None

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """Retrives the user credentials according to the param passed
            this depends if the credentials are valid both email and
            pwd
        Return:
            User.firsr_name (str)
            User.last_name (str)
            """

        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None

        try:
            from models.user import User
            users = User.search({"email": user_email})
            if not users:
                return None
            for user in users:
                if user.is_valid_password(user_pwd):
                    return user
        except Exception:
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Authenitcates the user credentials using all the previous defined
        methods above"""
        super().current_user(request)
        encoded_key =  self.extract_base64_authorization_header(
                self.authorization_header(request))
        decoded_key = self.decode_base64_authorization_header(encoded_key)
        user_email, user_pwd = self.extract_user_credentials(decoded_key)
        return self.user_object_from_credentials(user_email, user_pwd)
