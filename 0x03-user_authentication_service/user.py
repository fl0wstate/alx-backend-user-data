#!/usr/bin/env python3
"""Simple User Database"""
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class User(Base):
    """User class which will become the table in sql"""
    __tablename__ = 'users'

    id = Column('id', Integer, primary_key=True)
    email = Column('email', String(250), nullable=False)
    hashed_password = Column('hashed_password', String(250), nullable=False)
    session_id = Column('session_id', String(250), nullable=True)
    reset_token = Column('reset_token', String(250), nullable=True)



print(User.__tablename__)

for column in User.__table__.columns:
    print("{}: {}".format(column, column.type))
