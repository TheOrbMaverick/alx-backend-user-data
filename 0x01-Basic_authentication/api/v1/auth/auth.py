#!/usr/bin/env python3
"""
Auth module
"""
from flask import request
from typing import List, TypeVar
import fnmatch


class Auth:
    """Class to manage the API authentication"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Method to check if authentication is required"""
        if path is None:
            return True

        if excluded_paths is None or not excluded_paths:
            return True

        # Normalize path to ensure it ends with a slash
        if not path.endswith('/'):
            path += '/'

        for excluded_path in excluded_paths:
            # Normalize excluded_path to ensure it ends with a slash
            if not excluded_path.endswith('/'):
                excluded_path += '/'

            # Use fnmatch to handle wildcard matching
            if fnmatch.fnmatch(path, excluded_path):
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """Method to get the authorization header from the request"""
        if request is None:
            return None

        # Check if the Authorization header is present
        if 'Authorization' not in request.headers:
            return None

        # Return the value of the Authorization header
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """Method to get the current user from the request"""
        return None
