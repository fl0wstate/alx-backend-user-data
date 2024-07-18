#!/usr/bin/env python3
"""DB module
"""
from collections import UserString
from typing import Any, Dict
from sqlalchemy import create_engine
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Adds a user to the User database
            Return:
                returns the user object added to the database
        """
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        """Finds users from the database
        based on the keyword argumnent passed"""
        return self._session.query(User).filter_by(**kwargs).one()

    def update_user(self, user_id: int, **kwargs: Dict[str, Any]) -> None:
        """Updates the user matching the user_id passed
        Updates depends on the arbitary keywords args
        given that will be updated"""
        user = self.find_user_by(id=user_id)

        for key, val in kwargs.items():
            if not hasattr(User, key):
                raise ValueError
            else:
                setattr(user, key, val)
