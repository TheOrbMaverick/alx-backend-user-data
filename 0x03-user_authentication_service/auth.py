#!/usr/bin/env python3
"""
Auth module for handling password hashing.
"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


class Auth:
    """
    Auth class for password management.
    """
    def __init__(self) -> None:
        """
        Initialize the Auth class
        """
        self._db = DB()

    def _hash_password(password: str) -> bytes:
        """
        Hash a password with a salt.
        """
        salt = bcrypt.gensalt()
        hash_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hash_password
    
    def register_user(self, email: str, password: str) -> User:
        """
        Register a new user with email and password.
        """
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f'User {email} already exists')
        except NoResultFound:
            hashed_password = self._hash_password(password)
            user = self._db.add_user(email, hashed_password.decode('utf-8'))
            return user

    def valid_login(self, email: str, password: str) -> bool:
        """
        Validate the login credentials of a user.
        """
        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(password.encode('utf-8'), user.hashed_password.encode('utf-8'))
        except NoResultFound:
            return False
