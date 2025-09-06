from functools import wraps
from flask import request, jsonify, g
from utils.jwt_utils import JWTUtils
from persistence.user_repository import UserRepository

def jwt_required(f):
    """Decorator to protect routes with JWT authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None
        
        # Get token from Authorization header
        auth_header = request.headers.get('Authorization')
        if auth_header:
            try:
                token = auth_header.split(' ')[1]  # Bearer <token>
            except IndexError:
                return jsonify({
                    'status': 'error',
                    'message': 'Invalid authorization header format'
                }), 401
        
        if not token:
            return jsonify({
                'status': 'error',
                'message': 'Token is missing'
            }), 401
        
        # Decode token
        payload = JWTUtils.decode_token(token)
        if not payload:
            return jsonify({
                'status': 'error',
                'message': 'Token is invalid or expired'
            }), 401
        
        # Get user from database
        user_repo = UserRepository()
        user = user_repo.find_user_by_id(payload['user_id'])
        if not user:
            return jsonify({
                'status': 'error',
                'message': 'User not found'
            }), 401
        
        # Store user in Flask's g object for use in route
        g.current_user = user
        
        return f(*args, **kwargs)
    
    return decorated_function