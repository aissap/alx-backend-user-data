#!/usr/bin/env python3
"""Auth module"""
from typing import List, TypeVar
from flask import request
import fnmatch


class Auth:
    """Class to manage API authentication"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Check if path requires authentication"""
        if path is None or excluded_paths is None or not excluded_paths:
            return True
        if path[-1] != '/':
            path += '/'
        for excluded_path in excluded_paths:
            if excluded_path[-1] != '/':
                excluded_path += '/'
            if fnmatch.fnmatch(path, excluded_path):
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """Return None to indicate that no authorization header is present"""
        if request is None:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """Return None to indicate that no user is authenticated"""
        return None
