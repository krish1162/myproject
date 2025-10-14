from datetime import datetime, timedelta
import random
from utils.apps_data import generate_user_apps_and_games

# Mock session data - ADD THESE MISSING ARRAYS
devices = [
    {'name': 'Windows PC', 'os': 'Windows 10', 'browser': 'Chrome 115'},
    {'name': 'MacBook Pro', 'os': 'macOS Ventura', 'browser': 'Safari 16'},
    {'name': 'iPhone 12', 'os': 'iOS 16', 'browser': 'Mobile Safari'},
    {'name': 'Android Phone', 'os': 'Android 13', 'browser': 'Chrome Mobile'},
    {'name': 'Linux Desktop', 'os': 'Ubuntu 22.04', 'browser': 'Firefox 115'}
]

locations = [
    {'city': 'New York', 'country': 'USA', 'timezone': 'America/New_York'},
    {'city': 'London', 'country': 'UK', 'timezone': 'Europe/London'},
    {'city': 'Tokyo', 'country': 'Japan', 'timezone': 'Asia/Tokyo'},
    {'city': 'Sydney', 'country': 'Australia', 'timezone': 'Australia/Sydney'},
    {'city': 'San Francisco', 'country': 'USA', 'timezone': 'America/Los_Angeles'}
]

# Store user data in memory (in production, use a database)
user_sessions = {}
user_apps = {}  # NEW: Store user apps and games

def generate_mock_sessions_based_on_user(user_info, count=5):
    """Generate mock session data based on user information"""
    sessions = []
    for i in range(count):
        device = random.choice(devices)
        location = random.choice(locations)
        login_time = datetime.now() - timedelta(
            days=random.randint(0, 30), 
            hours=random.randint(0, 23),
            minutes=random.randint(0, 59)
        )
        
        sessions.append({
            'id': f'session_{i}',
            'device': device['name'],
            'os': device['os'],
            'browser': device['browser'],
            'location': f"{location['city']}, {location['country']}",
            'timezone': location['timezone'],
            'login_time': login_time.strftime('%Y-%m-%d %H:%M:%S'),
            'ip_address': f"192.168.{random.randint(0, 255)}.{random.randint(0, 255)}",
            'status': 'active' if random.random() > 0.3 else 'inactive',
            'current': i == 0  # Mark first session as current
        })
    
    return sessions

def get_user_apps(user_email):
    """Get user's connected apps and games"""
    if user_email not in user_apps:
        user_apps[user_email] = generate_user_apps_and_games(user_email)
    return user_apps[user_email]

def remove_user_app(user_email, app_id):
    """Remove an app/game from user's connected services"""
    if user_email in user_apps:
        user_apps[user_email] = [app for app in user_apps[user_email] if app['id'] != app_id]
    return True

def refresh_user_apps(user_email):
    """Refresh user's apps and games list"""
    user_apps[user_email] = generate_user_apps_and_games(user_email)
    return user_apps[user_email]