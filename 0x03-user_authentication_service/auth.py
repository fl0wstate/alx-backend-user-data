#!/usr/bin/env python3
"""Hashing password method"""
import bcrypt
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from db import DB
from user import User
import uuid


def _hash_password(password: str) -> bytes:
    """Hashes the password given through bcrypt"""
    return bcrypt.hashpw(
            password.encode(),
            bcrypt.gensalt())


def _generate_uuid() -> str:
    """returns a uuid string representation"""
    return str(uuid.uuid4())


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
            if (bcrypt.checkpw(password.encode(),
                               user.hashed_password)):
                return True
        except (InvalidRequestError, NoResultFound):
            return False

    def create_session(self, email: str) -> str:
        """creates a new session_id for user matching the email address"""
        if email:
            try:
                user = self._db.find_user_by(email=email)
                new_session_id = _generate_uuid()
                self._db.update_user(user.id, session_id=new_session_id)
            except (InvalidRequestError, NoResultFound):
                return None
            return new_session_id
        else:
            return None

    def get_user_from_session_id(
            self, session_id: str) -> User:
        """Returns a user based on the session_id given"""
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except (InvalidRequestError, NoResultFound):
            return None

    def destroy_session(self, user_id: int) -> None:
        """destroying user id session id"""
        if user_id:
            self._db.update_user(user_id, session_id=None)
        else:
            return None

    def get_reset_password_token(self, email: str) -> str:
        """Generates a reset token for the user table according
        to the email provided"""
        if email:
            try:
                user = self._db.find_user_by(email=email)
                self._db.update_user(user.id, reset_token=_generate_uuid())
                return user.reset_token
            except Exception:
                raise ValueError

    def update_password(self, reset_token, password):
        """Allows the program to update the user passwords"""
        if not reset_token or not password:
            return None

        try:
            user = self._db.find_user_by(reset_token=reset_token)
            hashed_pwd = _hash_password(password)
            self._db.update_user(user.id, hashed_password=hashed_pwd)
            self._db.update_user(user.id, reset_token=None)
        except Exception:
            raise ValueError
