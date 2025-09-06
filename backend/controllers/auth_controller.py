import bcrypt
import secrets
import datetime
from flask import Blueprint, request, jsonify
from persistence.user_repository import UserRepository
from models.user_model import User
from utils.jwt_utils import JWTUtils

auth_bp = Blueprint('auth', __name__)

# In-memory reset token store (use Redis/DB in production)
reset_tokens = {}

@auth_bp.route('/signup', methods=['POST'])
def signup():
    try:
        data = request.get_json()
        
        if not data or not all(k in data for k in ('name', 'email', 'password')):
            return jsonify({'status': 'error', 'message': 'Name, email, and password are required'}), 400
        
        name = data['name'].strip()
        email = data['email'].strip().lower()
        password = data['password']
        
        if len(name) < 2:
            return jsonify({'status': 'error', 'message': 'Name must be at least 2 characters long'}), 400
        if len(password) < 6:
            return jsonify({'status': 'error', 'message': 'Password must be at least 6 characters long'}), 400
        if '@' not in email or '.' not in email:
            return jsonify({'status': 'error', 'message': 'Please provide a valid email address'}), 400
        
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        user = User(name=name, email=email, password_hash=password_hash)
        user_repo = UserRepository()
        user_id = user_repo.create_user(user)
        
        token = JWTUtils.generate_token(user_id)
        
        return jsonify({
            'status': 'success',
            'message': 'User created successfully',
            'data': {
                'token': token,
                'user': {'id': user_id, 'name': name, 'email': email}
            }
        }), 201
    
    except ValueError as e:
        return jsonify({'status': 'error', 'message': str(e)}), 409
    except Exception:
        return jsonify({'status': 'error', 'message': 'An error occurred during signup'}), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        
        if not data or not all(k in data for k in ('email', 'password')):
            return jsonify({'status': 'error', 'message': 'Email and password are required'}), 400
        
        email = data['email'].strip().lower()
        password = data['password']
        
        user_repo = UserRepository()
        user = user_repo.find_user_by_email(email)
        
        if not user:
            return jsonify({'status': 'error', 'message': 'Invalid email or password'}), 401
        
        if not bcrypt.checkpw(password.encode('utf-8'), user['password_hash'].encode('utf-8')):
            return jsonify({'status': 'error', 'message': 'Invalid email or password'}), 401
        
        token = JWTUtils.generate_token(user['_id'])
        
        return jsonify({
            'status': 'success',
            'message': 'Login successful',
            'data': {
                'token': token,
                'user': {'id': user['_id'], 'name': user['name'], 'email': user['email']}
            }
        }), 200
    
    except Exception:
        return jsonify({'status': 'error', 'message': 'An error occurred during login'}), 500


@auth_bp.route('/forgot-password', methods=['POST'])
def forgot_password():
    try:
        data = request.get_json()
        
        if not data or 'email' not in data:
            return jsonify({'status': 'error', 'message': 'Email is required'}), 400
        
        email = data['email'].strip().lower()
        user_repo = UserRepository()
        user = user_repo.find_user_by_email(email)
        
        if not user:
            return jsonify({'status': 'error', 'message': 'User not found'}), 404
        
        # Generate reset token
        token = secrets.token_urlsafe(32)
        expiry = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        reset_tokens[token] = {'user_id': user['_id'], 'expires': expiry}
        
        # Normally send via email
        reset_link = f"http://localhost:3000/reset-password?token={token}"
        print(f"[DEBUG] Reset link for {email}: {reset_link}")
        
        return jsonify({'status': 'success', 'message': 'Password reset link sent'}), 200
    
    except Exception:
        return jsonify({'status': 'error', 'message': 'An error occurred during password reset request'}), 500


@auth_bp.route('/reset-password', methods=['POST'])
def reset_password():
    try:
        data = request.get_json()
        
        if not data or not all(k in data for k in ('token', 'password')):
            return jsonify({'status': 'error', 'message': 'Token and new password are required'}), 400
        
        token = data['token']
        new_password = data['password']
        
        if token not in reset_tokens:
            return jsonify({'status': 'error', 'message': 'Invalid or expired token'}), 400
        
        token_data = reset_tokens[token]
        if datetime.datetime.utcnow() > token_data['expires']:
            return jsonify({'status': 'error', 'message': 'Token expired'}), 400
        
        if len(new_password) < 6:
            return jsonify({'status': 'error', 'message': 'Password must be at least 6 characters long'}), 400
        
        password_hash = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        user_repo = UserRepository()
        user_repo.update_password(token_data['user_id'], password_hash)
        
        # Remove used token
        del reset_tokens[token]
        
        return jsonify({'status': 'success', 'message': 'Password reset successful'}), 200
    
    except Exception:
        return jsonify({'status': 'error', 'message': 'An error occurred during password reset'}), 500
