#!/usr/bin/env python3
"""BasicAuth module"""
import base64
from api.v1.auth.auth import Auth
from typing import Optional, Tuple
from models.user import User


class BasicAuth(Auth):
    """ Basic Authentication class """

    def extract_base64_authorization_header(self, authorization_header: str) -> Optional[str]:
        """Returns the Base64 part of the Authorization header for Basic Authentication."""
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header[6:]
