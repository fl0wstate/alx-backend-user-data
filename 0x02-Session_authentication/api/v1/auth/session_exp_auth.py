#!/usr/bin/env python3
"""Simple expiration session class handler"""
from .session_auth import SessionAuth
from os import getenv
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """SessionExpAuth modiefies each session by giving them a lifespan"""

    def __init__(self):
        """SessionExpAuth initializer method"""
        super().__init__()
        session_duration = getenv('SESSION_DURATION')
        if session_duration:
            if isinstance(int(session_duration), int):
                self.session_duration = int(session_duration)
        else:
            self.session_duration = 0

    def create_session(self, user_id: str = None) -> str:
        """creates a new session_dictionary under the user_id given"""
        session_id = super().create_session(user_id)
        if session_id:
            self.user_id_by_session_id[session_id] = {
                'user_id': user_id,
                'created_at': datetime.now()
            }
            return session_id
        return None

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """returns the user_id based on the session id passed"""
        if not session_id:
            return None
        session_dictionary = self.user_id_by_session_id[session_id]
        if session_dictionary is None:
            return None
        if session_dictionary:
            if self.session_duration <= 0:
                return session_dictionary.get('user_id')
            if 'created_at' not in session_dictionary:
                return None
            exp = session_dictionary['created_at'] + \
                timedelta(seconds=self.session_duration)
            if (exp < datetime.now()):
                return None
            return session_dictionary.get('user_id')
