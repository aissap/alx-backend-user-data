#!/usr/bin/env python3
"""BasicAuth module"""
from api.v1.auth.auth import Auth
from typing import Optional


class BasicAuth(Auth):
    def extract_base64_authorization_header(self, authorization_header: str) -> Optional[str]:
        """Extracts Base64  of the Authorization header for Basic Authentication."""
        if authorization_header is None or not isinstance(authorization_header, str):
            return None
        
        if not authorization_header.startswith("Basic "):
            return None
        
        return authorization_header.split(" ", 1)[-1].strip()