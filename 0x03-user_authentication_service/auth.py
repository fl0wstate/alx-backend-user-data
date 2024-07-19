#!/usr/bin/env python3
"""Hashing password method"""

import bcrypt
from sqlalchemy.exc import InvalidRequestError, NoResultFound
from db import DB
from user import User


def _hash_password(password: str) -> bytes:
    """Hashes the password given through bcrypt"""
    return bcrypt.hashpw(
            password.encode(),
            bcrypt.gensalt())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """Constructor for the datbase function"""
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """returns a user whose password has been hashed when
        registered to the datbase"""
        # find the user by email
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except (InvalidRequestError, NoResultFound):
            pass

        hashed_pass = _hash_password(password)
        return self._db.add_user(email, hashed_pass)

    def valid_login(self, email: str, password: str) -> bool:
        """checks for matching passwords"""
        if not email or not password:
            return False
        try:
            user = self._db.find_user_by(email=email)
            if (bcrypt.checkpw(
                user.hashed_password,
                password.encode()
            )):
                return True
        except (InvalidRequestError, NoResultFound):
            return False
