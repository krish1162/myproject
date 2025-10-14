from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from functools import wraps
from config import Config
from utils.google_auth import GoogleAuth
from utils.data_utils import user_sessions, generate_mock_sessions_based_on_user
# Add this import at the top - CORRECTED
from utils.data_utils import get_user_apps, remove_user_app, refresh_user_apps

app = Flask(__name__)
app.config.from_object(Config)

def login_required(f):
    """Decorator to ensure user is logged in"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session or 'access_token' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    if 'user' in session and 'access_token' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/google-login')
def google_login():
    """Redirect to Google OAuth 2.0 authentication"""
    auth_url = GoogleAuth.get_auth_url()
    return redirect(auth_url)

@app.route('/auth/callback')
def auth_callback():
    """Handle Google OAuth 2.0 callback"""
    code = request.args.get('code')
    error = request.args.get('error')
    
    if error:
        return f"Authorization failed: {error}", 400
    
    try:
        # Exchange authorization code for tokens
        tokens = GoogleAuth.exchange_code_for_token(code)
        access_token = tokens['access_token']
        
        # Get user information
        user_info = GoogleAuth.get_user_info(access_token)
        
        # Store user info and tokens in session
        session['user'] = user_info
        session['access_token'] = access_token
        session['refresh_token'] = tokens.get('refresh_token')
        
        # Generate mock sessions for the user
        user_sessions[user_info['email']] = generate_mock_sessions_based_on_user(user_info)
        
        return redirect(url_for('dashboard'))
        
    except Exception as e:
        return f"Authentication failed: {str(e)}", 400

# Add these new routes after the existing routes - CORRECTED

@app.route('/apps')
@login_required
def apps_management():
    """Show connected apps and games"""
    user_email = session['user']['email']
    user_apps_list = get_user_apps(user_email)
    
    # Calculate stats
    total_apps = len(user_apps_list)
    active_apps = sum(1 for app in user_apps_list if app['status'] == 'active')
    
    return render_template(
        'apps.html',
        user=session['user'],
        apps=user_apps_list,
        total_apps=total_apps,
        active_apps=active_apps
    )

@app.route('/remove_app/<app_id>', methods=['POST'])
@login_required
def remove_app(app_id):
    """Remove an app/game from connected services"""
    user_email = session['user']['email']
    
    try:
        success = remove_user_app(user_email, app_id)
        if success:
            return jsonify({'success': True, 'message': 'App access removed successfully'})
        else:
            return jsonify({'success': False, 'message': 'App not found'}), 404
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/refresh_apps')
@login_required
def refresh_apps():
    """Refresh the apps and games list"""
    user_email = session['user']['email']
    refresh_user_apps(user_email)
    return redirect(url_for('apps_management'))

# Update the dashboard route to include apps link - CORRECTED
@app.route('/dashboard')
@login_required
def dashboard():
    user_info = session['user']
    user_email = user_info['email']
    
    # Get user sessions
    sessions = user_sessions.get(user_email, [])
    
    # Count active sessions
    active_sessions = sum(1 for s in sessions if s['status'] == 'active')
    
    # Get apps count for the dashboard
    user_apps_list = get_user_apps(user_email)
    total_apps = len(user_apps_list)
    active_apps = sum(1 for app in user_apps_list if app['status'] == 'active')
    
    return render_template(
        'dashboard.html', 
        user=user_info, 
        sessions=sessions,
        active_sessions=active_sessions,
        total_apps=total_apps,
        active_apps=active_apps
    )

@app.route('/logout_session/<session_id>', methods=['POST'])
@login_required
def logout_session(session_id):
    user_email = session['user']['email']
    sessions = user_sessions.get(user_email, [])
    
    # Find the session and mark it as inactive
    for s in sessions:
        if s['id'] == session_id:
            s['status'] = 'inactive'
            return jsonify({'success': True, 'message': 'Session logged out successfully'})
    
    return jsonify({'success': False, 'message': 'Session not found'}), 404

@app.route('/refresh_sessions')
@login_required
def refresh_sessions():
    user_email = session['user']['email']
    # Regenerate sessions
    user_sessions[user_email] = generate_mock_sessions_based_on_user(session['user'])
    return redirect(url_for('dashboard'))

@app.route('/logout')
def logout():
    """Logout and revoke Google tokens"""
    if 'access_token' in session:
        # Revoke the access token with Google
        GoogleAuth.revoke_token(session['access_token'])
    
    # Clear session
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)