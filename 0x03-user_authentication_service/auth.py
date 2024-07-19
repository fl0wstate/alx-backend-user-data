#!/usr/bin/env python3
"""Hashing password method"""

import bcrypt


def _hash_password(password: str) -> bytes:
    """Hashes the password given through bcrypt"""
    return bcrypt.hashpw(
            password.encode('utf-8'),
            bcrypt.gensalt())
