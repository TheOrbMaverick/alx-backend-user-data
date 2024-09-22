#!/usr/bin/env python3
"""
encrypt_password module
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """
    Hashes a password with a salt using bcrypt and returns the salted, hashed password.
    
    Args:
        password (str): The password to hash.
    
    Returns:
        bytes: The salted, hashed password as a byte string.
    """
    # Generate a salt
    salt = bcrypt.gensalt()
    
    # Return the hashed password with the salt
    return bcrypt.hashpw(password.encode('utf-8'), salt)


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Validates that the provided password matches the hashed password.
    
    Args:
        hashed_password (bytes): The hashed password.
        password (str): The plain text password to verify.
    
    Returns:
        bool: True if the password matches, False otherwise.
    """
    # Check if the provided password matches the hashed password
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
