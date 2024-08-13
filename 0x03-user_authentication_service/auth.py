#!/usr/bin/env python3
"""
Auth module for handling password hashing.
"""
import bcrypt
from db import DB
import uuid
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
        
    def _generate_uuid(self) -> str:
        """
        Generate a new UUID.
        """
        return str(uuid.uuid4())
    
    def create_session(self, email: str) -> str:
        """
        Create a session ID for a user.
        """
        try:
            user = self._db.find_user_by(email=email)
            session_id = self._generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return ""
        
    def get_user_from_session_id(self, session_id: str) -> User:
        """
        Get a user from a session ID.
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
        Destroy a user's session by setting their session ID to None.
        """
        try:
            self._db.update_user(user_id, session_id=None)
        except NoResultFound:
            pass

    def get_reset_password_token(self, email: str) -> str:
        """
        Generate a reset password token for the user.
        """
        try:
            user = self._db.find_user_by(email=email)
            reset_token = self._generate_uuid()
            self._db.update_user(user.id, reset_token=reset_token)
            return reset_token
        except NoResultFound:
            raise ValueError("User not found")
        
    def update_password(self, reset_token: str, password: str) -> None:
        """
        Update the user's password using the reset token.
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            hashed_password = self._hash_password(password)
            self._db.update_user(user.id, hashed_password=hashed_password, reset_token=None)
        except:
            raise ValueError("Invalid reset token")
