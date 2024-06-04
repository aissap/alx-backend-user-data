#!/usr/bin/env python3
"""Manage the API authentication.
"""
from typing import List, TypeVar
from flask import request


class Auth:
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """checking if authentication is required"""
        if path is None or excluded_paths is None or len(excluded_paths) == 0:
            return True
        path = path.rstrip('/') + '/'
        excluded_paths = [p.rstrip('/') + '/' for p in excluded_paths]
        return path not in excluded_paths

    def authorization_header(self, request=None) -> str:
        """Retrieving the authorization header from the request."""
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Retrieving the current user from the request."""
        return None
