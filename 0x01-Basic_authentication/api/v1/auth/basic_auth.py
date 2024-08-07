#!/usr/bin/env python3
"""
BasicAuth module
"""
import base64
from api.v1.auth.auth import Auth
from models.user import User


class BasicAuth(Auth):
    """Class to manage basic API authentication"""

    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """Method to extract the Base64 part of the Authorization header"""
        if authorization_header is None:
            return None

        if not isinstance(authorization_header, str):
            return None

        if not authorization_header.startswith("Basic "):
            return None

        return authorization_header.split(" ", 1)[1]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """Method to decode the Base64 part of the Authorization header"""
        if base64_authorization_header is None:
            return None

        if not isinstance(base64_authorization_header, str):
            return None

        try:
            base64_bytes = base64_authorization_header.encode('utf-8')
            decoded_bytes = base64.b64decode(base64_bytes)
            return decoded_bytes.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """
        Method to extract user email and password from the Base64 decoded value
        """
        if decoded_base64_authorization_header is None:
            return None, None

        if not isinstance(decoded_base64_authorization_header, str):
            return None, None

        if ':' not in decoded_base64_authorization_header:
            return None, None

        email, password = decoded_base64_authorization_header.split(':', 1)
        return email, password

    def user_object_from_credentials(self, user_email: str, user_pwd: str):
        """
        Method to return the User instance based on his email and password
        """
        if user_email is None or not isinstance(user_email, str):
            return None

        if user_pwd is None or not isinstance(user_pwd, str):
            return None

        # Search for the user by email
        user_list = User.search({'email': user_email})

        if not user_list:
            return None

        user = user_list[0]

        # Validate the user's password
        if not user.is_valid_password(user_pwd):
            return None

        return user

    def current_user(self, request=None):
        """Method to retrieve the User instance for a request"""
        auth_header = self.authorization_header(request)
        if auth_header is None:
            return None

        base64_auth_header = self.extract_base64_authorization_header(
            auth_header
            )
        if base64_auth_header is None:
            return None

        decoded_auth_header = self.decode_base64_authorization_header(
            base64_auth_header
            )
        if decoded_auth_header is None:
            return None

        user_email, user_pwd = self.extract_user_credentials(
            decoded_auth_header
            )
        if user_email is None or user_pwd is None:
            return None

        user = self.user_object_from_credentials(user_email, user_pwd)
        return user
