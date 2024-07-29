#!/usr/bin/env python3
"""Session authentication storage for session id"""

from datetime import datetime, timedelta
from .session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """Session storage handler"""

    def create_session(self, user_id: str = None) -> str:
        """Session creator same as SessionExpAuth"""
        session = super().create_session(user_id)

        if not session:
            return None

        user_session_id = UserSession(user_id=user_id, session_id=session)
        user_session_id.save()
        return session

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Getting the session id from the session_id files"""
        if session_id is None:
            return None

        UserSession.load_from_file()
        result = UserSession.search({'session_id': session_id})
        if result is None:
            return None

        user_session_id = result[0]

        timeD = user_session_id.created_at + \
            timedelta(seconds=self.session_duration)

        if timeD < datetime.utcnow():
            return None

        return user_session_id.get('user_id')

    def destroy_session(self, request=None) -> bool:
        """Destroyes the user session and
        returns True if the command was succesfull"""
        if request is None:
            return False

        session_id = self.session_cookie(request)
        if session_id is None:
            return False

        user_session_id = UserSession.search({'session_id': session_id})
        if user_session_id is None:
            return False

        session = user_session_id[0]
        session.remove()
        return True
