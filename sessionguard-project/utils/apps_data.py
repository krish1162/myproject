# Comprehensive list of popular apps and games that use Google login
POPULAR_APPS = [
    {
        'id': 'spotify',
        'name': 'Spotify',
        'category': 'Music',
        'icon': 'fas fa-music',
        'color': '#1DB954',
        'permissions': ['View your email address', 'Access your profile info'],
        'login_date': None,
        'status': 'active'
    },
    {
        'id': 'netflix',
        'name': 'Netflix',
        'category': 'Entertainment',
        'icon': 'fas fa-tv',
        'color': '#E50914',
        'permissions': ['View your email address', 'Access your profile info'],
        'login_date': None,
        'status': 'active'
    },
    {
        'id': 'instagram',
        'name': 'Instagram',
        'category': 'Social Media',
        'icon': 'fab fa-instagram',
        'color': '#E4405F',
        'permissions': ['View your email address', 'Access your profile info', 'Post on your behalf'],
        'login_date': None,
        'status': 'active'
    },
    {
        'id': 'airbnb',
        'name': 'Airbnb',
        'category': 'Travel',
        'icon': 'fas fa-home',
        'color': '#FF5A5F',
        'permissions': ['View your email address', 'Access your profile info'],
        'login_date': None,
        'status': 'active'
    },
    {
        'id': 'uber',
        'name': 'Uber',
        'category': 'Transportation',
        'icon': 'fas fa-car',
        'color': '#000000',
        'permissions': ['View your email address', 'Access your profile info', 'View your location'],
        'login_date': None,
        'status': 'active'
    },
    {
        'id': 'dropbox',
        'name': 'Dropbox',
        'category': 'Productivity',
        'icon': 'fab fa-dropbox',
        'color': '#0061FF',
        'permissions': ['View your email address', 'Access your files'],
        'login_date': None,
        'status': 'active'
    },
    {
        'id': 'asana',
        'name': 'Asana',
        'category': 'Productivity',
        'icon': 'fas fa-tasks',
        'color': '#FF6361',
        'permissions': ['View your email address', 'Manage your tasks'],
        'login_date': None,
        'status': 'active'
    }
]

POPULAR_GAMES = [
    {
        'id': 'minecraft',
        'name': 'Minecraft',
        'category': 'Gaming',
        'icon': 'fas fa-cube',
        'color': '#6CC416',
        'permissions': ['View your email address', 'Access your profile info', 'Save game data'],
        'login_date': None,
        'status': 'active'
    },
    {
        'id': 'fortnite',
        'name': 'Fortnite',
        'category': 'Gaming',
        'icon': 'fas fa-gamepad',
        'color': '#C3C3C3',
        'permissions': ['View your email address', 'Access your profile info', 'Save game progress'],
        'login_date': None,
        'status': 'active'
    },
    {
        'id': 'among_us',
        'name': 'Among Us',
        'category': 'Gaming',
        'icon': 'fas fa-user-astronaut',
        'color': '#FF5555',
        'permissions': ['View your email address', 'Access your profile info'],
        'login_date': None,
        'status': 'active'
    },
    {
        'id': 'pubg',
        'name': 'PUBG Mobile',
        'category': 'Gaming',
        'icon': 'fas fa-crosshairs',
        'color': '#FFA500',
        'permissions': ['View your email address', 'Access your profile info', 'Save game data'],
        'login_date': None,
        'status': 'active'
    },
    {
        'id': 'cod',
        'name': 'Call of Duty',
        'category': 'Gaming',
        'icon': 'fas fa-gun',
        'color': '#FF0000',
        'permissions': ['View your email address', 'Access your profile info', 'Save game progress'],
        'login_date': None,
        'status': 'active'
    },
    {
        'id': 'roblox',
        'name': 'Roblox',
        'category': 'Gaming',
        'icon': 'fas fa-robot',
        'color': '#FF0000',
        'permissions': ['View your email address', 'Access your profile info', 'Save game data'],
        'login_date': None,
        'status': 'active'
    }
]

def generate_user_apps_and_games(user_email, count=8):
    """Generate mock apps and games that user has logged into"""
    import random
    from datetime import datetime, timedelta
    
    all_services = POPULAR_APPS + POPULAR_GAMES
    selected_services = random.sample(all_services, min(count, len(all_services)))
    
    user_services = []
    for service in selected_services:
        # Create a copy to avoid modifying the original
        service_copy = service.copy()
        # Set random login date (within last year)
        days_ago = random.randint(1, 365)
        service_copy['login_date'] = (datetime.now() - timedelta(days=days_ago)).strftime('%Y-%m-%d')
        service_copy['last_used'] = (datetime.now() - timedelta(days=random.randint(0, days_ago))).strftime('%Y-%m-%d')
        service_copy['status'] = 'active' if random.random() > 0.2 else 'inactive'
        user_services.append(service_copy)
    
    return user_services

def get_app_categories():
    """Get all available app categories"""
    categories = set()
    for app in POPULAR_APPS + POPULAR_GAMES:
        categories.add(app['category'])
    return sorted(list(categories))