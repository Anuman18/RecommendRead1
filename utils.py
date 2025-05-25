from functools import wraps
from flask import session, jsonify

def login_required(f):
    """
    Decorator to check if a user is logged in.
    If not, returns a 401 Unauthorized response.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': 'Authentication required'}), 401
        return f(*args, **kwargs)
    return decorated_function
