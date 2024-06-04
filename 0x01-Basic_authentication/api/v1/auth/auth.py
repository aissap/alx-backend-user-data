#!/usr/b`:in/env python3
"""Manage the API authentication.
"""
from typing import List, TypeVar
from flask import request


class Auth:
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """checking if authentication is required"""
        if path is None:
            return True
        if excluded_paths is None or len(excluded_paths) == 0:
            return True
        for excluded_path in excluded_paths:
            if path.rstrip('/') == excluded_path.rstrip('/'):
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """Retrieving the authorization header from the request."""
        if request is not None:
            return request.headers.get('Authorization', None)    
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Retrieving the current user from the request."""
        return None
