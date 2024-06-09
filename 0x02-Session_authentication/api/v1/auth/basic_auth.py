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


    def decode_base64_authorization_header(self, base64_authorization_header: str) -> Optional[str]:
        """Decodes the Base64 part of the Authorization header."""
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            decoded_bytes = base64.b64decode(base64_authorization_header)
            return decoded_bytes.decode('utf-8')
        except Exception:
            return None


    def extract_user_credentials(self, decoded_base64_authorization_header: str) -> Optional[Tuple[str, str]]:
        """Extracts user credentials from the decoded value."""
        if decoded_base64_authorization_header is None:
            return None, None
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None

        user_email, user_pwd = decoded_base64_authorization_header.split(':', 1)
        return user_email, user_pwd

        
