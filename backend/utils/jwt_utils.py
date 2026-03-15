import os
import jwt
from datetime import datetime, timedelta
from typing import Dict, Optional

class JWTUtils:
    @staticmethod
    def _get_secret_key() -> str:
        return os.getenv('JWT_SECRET_KEY', 'mimicker-dev-secret-key')

    @staticmethod
    def generate_token(user_id: str) -> str:
        """Generate JWT token for user"""
        payload = {
            'user_id': user_id,
            'exp': datetime.utcnow() + timedelta(days=7),  # Token expires in 7 days
            'iat': datetime.utcnow()
        }
        
        secret_key = JWTUtils._get_secret_key()
        return jwt.encode(payload, secret_key, algorithm='HS256')
    
    @staticmethod
    def decode_token(token: str) -> Optional[Dict]:
        """Decode JWT token and return payload"""
        try:
            secret_key = JWTUtils._get_secret_key()
            payload = jwt.decode(token, secret_key, algorithms=['HS256'])
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
