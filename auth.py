import os
import functools
from flask import request, Response, session, redirect, url_for, flash, abort

def check_auth(username, password):
    """Check if username/password combination is valid."""
    admin_username = os.environ.get('ADMIN_USERNAME', 'admin')
    admin_password = os.environ.get('ADMIN_PASSWORD', 'admin123')
    return username == admin_username and password == admin_password

def authenticate():
    """Send a 401 response that enables basic auth"""
    return Response(
        'Could not verify your access level for that URL.\n'
        'You have to login with proper credentials', 401,
        {'WWW-Authenticate': 'Basic realm="Admin Area"'})

def check_ip_access():
    """Check if the current IP is allowed to access admin"""
    allowed_ips = os.environ.get('ADMIN_ALLOWED_IPS', '').split(',')
    allowed_ips = [ip.strip() for ip in allowed_ips if ip.strip()]
    
    # If no IPs are configured, allow all (for development)
    if not allowed_ips:
        return True
    
    # Get the real IP address (considering proxies)
    real_ip = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
    if real_ip:
        real_ip = real_ip.split(',')[0].strip()
    
    return real_ip in allowed_ips

def requires_auth(f):
    """Decorator that requires HTTP basic authentication and IP whitelist"""
    @functools.wraps(f)
    def decorated(*args, **kwargs):
        # First check IP access
        if not check_ip_access():
            abort(404)  # Return 404 instead of 403 to hide the existence of admin
        
        # Then check authentication
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

def session_auth_required(f):
    """Alternative session-based auth decorator"""
    @functools.wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('admin_authenticated'):
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated