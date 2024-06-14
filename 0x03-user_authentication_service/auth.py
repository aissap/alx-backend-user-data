#!/usr/bin/env python3
"""
Auth module
"""
import uuid
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _generate_uuid() -> str:
    """
    Generate a new UUID and return it as a string.
    """
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def _hash_password(self, password: str) -> bytes:
        """
        Hash a password with bcrypt.
        """
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed

    def register_user(self, email: str, password: str) -> User:
        """
        Register a new user with email and password.
        """
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hashed_password = self._hash_password(password)
            new_user = self._db.add_user(
                    email,
                    hashed_password.decode('utf-8')
                    )
            return new_user

    def valid_login(self, email: str, password: str) -> bool:
        """Validates user credentials.
        """
        try:
            user = self._db.find_user_by(email=email)
            if user is not None:
                return bcrypt.checkpw(
                        password.encode("utf-8"),
                        user.hashed_password.encode("utf-8"))
        except NoResultFound:
            pass
        return False

    def create_session(self, email: str) -> str:
        """
        Create a session for the user identified by email.
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None

        new_session_id = _generate_uuid()
        self._db.update_user(user.id, session_id=new_session_id)
        return new_session_id

    def get_user_from_session_id(self, session_id: str) -> User:
        """
        Find the user corresponding to the given session ID.
        """
        if session_id is None:
            return None

        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """
        Destroy a session.
        """
        try:
            user = self._db.find_user_by(id=user_id)
            self._db.update_user(user.id, session_id=None)
        except NoResultFound:
            pass

    def get_reset_password_token(self, email: str) -> str:
        """Generate reset password token.
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError(f"User with email '{email}' not found")

        reset_token = str(uuid.uuid4())

        self._db.update_user(user.id, reset_token=reset_token)

        return reset_token