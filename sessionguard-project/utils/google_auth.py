import json
import requests
from flask import session, redirect
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from config import Config

class GoogleAuth:
    @staticmethod
    def get_auth_url():
        """Generate Google OAuth 2.0 authorization URL"""
        auth_url = (
            "https://accounts.google.com/o/oauth2/v2/auth?"
            "response_type=code&"
            f"client_id={Config.GOOGLE_CLIENT_ID}&"
            f"redirect_uri={Config.REDIRECT_URI}&"
            f"scope={'+'.join(Config.SCOPES)}&"
            "access_type=offline&"
            "prompt=consent"
        )
        return auth_url

    @staticmethod
    def exchange_code_for_token(code):
        """Exchange authorization code for access token"""
        token_url = "https://oauth2.googleapis.com/token"
        data = {
            'code': code,
            'client_id': Config.GOOGLE_CLIENT_ID,
            'client_secret': Config.GOOGLE_CLIENT_SECRET,
            'redirect_uri': Config.REDIRECT_URI,
            'grant_type': 'authorization_code'
        }
        
        response = requests.post(token_url, data=data)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Token exchange failed: {response.text}")

    @staticmethod
    def get_user_info(access_token):
        """Get user information using access token"""
        userinfo_url = "https://www.googleapis.com/oauth2/v2/userinfo"
        headers = {'Authorization': f'Bearer {access_token}'}
        
        response = requests.get(userinfo_url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to get user info: {response.text}")

    @staticmethod
    def get_active_sessions(access_token):
        """Get active sessions from Google Account (Note: This is a simulation)"""
        # Note: Google doesn't provide a direct API to get active sessions
        # This is a simulation using the user's info and some mock data
        user_info = GoogleAuth.get_user_info(access_token)
        
        # In a real implementation, you would need to use Google's Admin SDK
        # or Security APIs which require additional permissions and verification
        from utils.data_utils import generate_mock_sessions_based_on_user
        
        sessions = generate_mock_sessions_based_on_user(user_info)
        return sessions

    @staticmethod
    def revoke_token(token):
        """Revoke access token to log out"""
        revoke_url = "https://oauth2.googleapis.com/revoke"
        data = {'token': token}
        response = requests.post(revoke_url, data=data)
        return response.status_code == 200