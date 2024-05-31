#!/usr/bin/env python3
"""
Encrypt Password
"""

import bcrypt


def hash_password(password: str) -> bytes:
    """Hashing password, which is a byte string."""
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Matching password to its  hashed version."""
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
