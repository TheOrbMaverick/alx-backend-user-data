#!/usr/bin/env python3
"""
SessionAuth module for managing session authentication
"""
from api.v1.auth.auth import Auth
import uuid
from typing import TypeVar
from models.user import User


class SessionAuth(Auth):
    """SessionAuth class that inherits from Auth"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Create a session ID for a user ID"""
        if user_id is None or not isinstance(user_id, str):
            return None
        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Retrieve a User ID based on a Session ID"""
        if session_id is None or not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """Retrieve the User instance based on the session ID in the cookie"""

        # Ensure the request object is provided
        if request is None:
            return None

        # Get the session ID from the request cookies
        session_id = self.session_cookie(request)

        # If no session ID is present in the cookies, return None
        if session_id is None:
            return None

        # Get the user ID associated with the session ID
        user_id = self.user_id_for_session_id(session_id)

        # If the session ID is not valid or has no associated user, return None
        if user_id is None:
            return None

        # Use the user ID to retrieve the User instance from the database
        return User.get(user_id)

    def destroy_session(self, request=None) -> bool:
        """Deletes the user session / logout"""
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if session_id is None:
            return False
        if not self.user_id_for_session_id(session_id):
            return False
        del self.user_id_by_session_id[session_id]
        return True
