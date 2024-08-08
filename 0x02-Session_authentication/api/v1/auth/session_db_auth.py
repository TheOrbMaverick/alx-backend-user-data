#!/usr/bin/env python3
""" SessionDBAuth module for session-based authentication with database storage """
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """ SessionDBAuth class for session-based authentication with database storage """
    
    def create_session(self, user_id=None):
        """ Creates a session ID for a user_id and stores it in the database """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        
        user_session = UserSession(user_id=user_id, session_id=session_id)
        user_session.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """ Returns a User ID based on a Session ID from the database """
        if session_id is None:
            return None
        UserSession.load_from_file()
        sessions = UserSession.search({'session_id': session_id})
        if not sessions:
            return None
        session = sessions[0]
        return session.user_id

    def destroy_session(self, request=None):
        """ Destroys the UserSession based on the Session ID from the request cookie """
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if session_id is None:
            return False
        UserSession.load_from_file()
        sessions = UserSession.search({'session_id': session_id})
        if not sessions:
            return False
        session = sessions[0]
        session.remove()
        return True
