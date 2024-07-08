#!/usr/bin/env python3
"""Using the bcrypt to hash users database passwords"""
import bcrypt
from typing import Any


def hash_password(password: Any) -> bytes:
    """generate hashed passwords using bcrypt algorithm"""
    _salt = bcrypt.gensalt()
    bits = password.encode('utf-8')
    new_pwd = bcrypt.hashpw(bits, _salt)
    return new_pwd
