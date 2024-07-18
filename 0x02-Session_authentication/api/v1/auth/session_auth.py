#!/usr/bin/env python
"""Creating a session cookie"""

from .auth import Auth
from typing import TypeVar
import uuid


class SessionAuth(Auth):
    """session class creator"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """instance method that creates a session id for the
        user id passed"""
        if user_id is None:
            return None
        if not isinstance(user_id, str):
            return None
        else:
            try:
                session_id = str(uuid.uuid4())
                self.user_id_by_session_id[session_id] = user_id
                return session_id
            except Exception as e:
                print(f"Error Generating Session ID: [<{e}>]")

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """retriving user_id from the user_id_by_session_id dict"""
        if session_id is None:
            return None
        if not isinstance(session_id, str):
            return None
        else:
            try:
                user_id = str(self.user_id_by_session_id.get(session_id))
                return user_id
            except Exception as e:
                print(f"Error retriving data from the dict: [<{e}>]")

    def current_user(self, request=None) -> TypeVar('User'):
        """Retrives the current user from the database
        depending of the user session cookie"""
        super().current_user(request)
        try:
            cookie = self.session_cookie(request)
            user_id = self.user_id_for_session_id(cookie)

            from models.user import User
            found_user = User.get(user_id)
            return found_user
        except Exception:
            return None

    def destroy_session(self, request=None) -> bool:
        """Destroying all the session id created for the user_id"""
        if not request:
            return False
        SESSION = self.session_cookie(request)
        if not SESSION:
            return False
        if not self.user_id_for_session_id(SESSION):
            return False
        print("_____[ SESSION ]____")
        print(SESSION)
        print("_____[ DICT ]____")
        print(self.user_id_by_session_id)
        print("_____[ VAL ]____")
        print(self.user_id_by_session_id.get(SESSION))
        if self.user_id_by_session_id.pop(SESSION, None):
           return True
        


        return True


        
