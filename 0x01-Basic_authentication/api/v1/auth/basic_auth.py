#!/usr/bin/env python3
"""BasicAuth module"""
from api.v1.auth.auth import Auth
from typing import Optional


class BasicAuth(Auth):
    """Basic auth."""
    def extract_base64_authorization_header(self, authorization_header: str) -> Optional[str]:
        """returns the Base64 part of the Authorization header for a Basic Authentication."""
        if authorization_header is None:
            return None
        elif not isinstance(authorization_header, str):
            return None
        elif not authorization_header.startswith("Basic "):
            return None
        
        parts = authorization_header.split(" ", 1)

        if len(parts) != 2:
            return None
        
        return parts[1].strip()

    def decode_base64_authorization_header(self, base64_authorization_header: str) -> Optional[str]:
        """Returns the decoded value."""
        if base64_authorization_header is None or not isinstance(base64_authorization_header, str):
            return None
        
        try:
            decoded_bytes = base64.b64decode(base64_authorization_header)
            decoded_str = decoded_bytes.decode('utf-8')
            return decoded_str
        except:
            return None