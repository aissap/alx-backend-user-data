#!/usr/bin/env python3
"""Manage the API authentication.
"""
from typing import List, TypeVar
from flask import request

User = TypeVar('User')

class Auth:
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """checking if authentication """
        return False

    def authorization_header(self, request=None) -> str:
        """Retrieving the authorization header from the request."""
        return None

    def current_user(self, request=None) -> User:
        """Retrieving the current user from the request."""