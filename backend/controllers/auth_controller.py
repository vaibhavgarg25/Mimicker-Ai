import bcrypt
from flask import Blueprint, request, jsonify
from persistence.user_repository import UserRepository
from models.user_model import User
from utils.jwt_utils import JWTUtils

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/signup', methods=['POST'])
def signup():
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data or not all(k in data for k in ('name', 'email', 'password')):
            return jsonify({
                'status': 'error',
                'message': 'Name, email, and password are required'
            }), 400
        
        name = data['name'].strip()
        email = data['email'].strip().lower()
        password = data['password']
        
        # Basic validation
        if len(name) < 2:
            return jsonify({
                'status': 'error',
                'message': 'Name must be at least 2 characters long'
            }), 400
        
        if len(password) < 6:
            return jsonify({
                'status': 'error',
                'message': 'Password must be at least 6 characters long'
            }), 400
        
        if '@' not in email or '.' not in email:
            return jsonify({
                'status': 'error',
                'message': 'Please provide a valid email address'
            }), 400
        
        # Hash password
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        # Create user
        user = User(name=name, email=email, password_hash=password_hash)
        user_repo = UserRepository()
        
        user_id = user_repo.create_user(user)
        
        # Generate JWT token
        token = JWTUtils.generate_token(user_id)
        
        return jsonify({
            'status': 'success',
            'message': 'User created successfully',
            'data': {
                'token': token,
                'user': {
                    'id': user_id,
                    'name': name,
                    'email': email
                }
            }
        }), 201
    
    except ValueError as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 409
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'An error occurred during signup'
        }), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data or not all(k in data for k in ('email', 'password')):
            return jsonify({
                'status': 'error',
                'message': 'Email and password are required'
            }), 400
        
        email = data['email'].strip().lower()
        password = data['password']
        
        # Find user by email
        user_repo = UserRepository()
        user = user_repo.find_user_by_email(email)
        
        if not user:
            return jsonify({
                'status': 'error',
                'message': 'Invalid email or password'
            }), 401
        
        # Verify password
        if not bcrypt.checkpw(password.encode('utf-8'), user['password_hash'].encode('utf-8')):
            return jsonify({
                'status': 'error',
                'message': 'Invalid email or password'
            }), 401
        
        # Generate JWT token
        token = JWTUtils.generate_token(user['_id'])
        
        return jsonify({
            'status': 'success',
            'message': 'Login successful',
            'data': {
                'token': token,
                'user': {
                    'id': user['_id'],
                    'name': user['name'],
                    'email': user['email']
                }
            }
        }), 200
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'An error occurred during login'
        }), 500
