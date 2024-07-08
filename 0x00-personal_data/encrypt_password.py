#!/usr/bin/env python3
"""Using the bcrypt to hash users database passwords"""
import bcrypt


def hash_password(password: str) -> bytes:
    """generate hashed passwords using bcrypt algorithm"""
    _salt = bcrypt.gensalt()
    bits = password.encode()
    new_pwd = bcrypt.hashpw(bits, _salt)
    return new_pwd


def is_valid(hashed_password: bytes, password: str) -> bool:
    """validates the hashed passwords"""
    return (bcrypt.checkpw(password.encode(), hashed_password))
