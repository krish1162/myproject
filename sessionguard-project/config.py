import os

class Config:
    # Google OAuth 2.0 credentials - You need to get these from Google Cloud Console
    GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID', '')
    GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET', '')
    
    # Flask configuration
    SECRET_KEY = os.environ.get('SESSIONGUARD_SECRET_KEY', 'your-secret-key-here')
    
    # Google API scopes
    SCOPES = [
        'https://www.googleapis.com/auth/userinfo.email',
        'https://www.googleapis.com/auth/userinfo.profile',
        'openid'
    ]
    
    # Redirect URI - Update this with your actual domain in production
    REDIRECT_URI = 'http://localhost:5000/auth/callback'