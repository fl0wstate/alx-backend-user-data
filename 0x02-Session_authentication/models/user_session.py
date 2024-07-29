#!/usr/bin/env python3
"""Memory storage for all the user session"""
from .base import Base


class UserSession(Base):
    """UserSession storage unit"""

    def __init__(self, *args: list, **kwargs: dict):
        """class initalizer"""
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')
