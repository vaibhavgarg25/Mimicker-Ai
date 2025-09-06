import os
import jwt
from datetime import datetime, timedelta
from typing import Dict, Optional

class JWTUtils:
    @staticmethod
    def generate_token(user_id: str) -> str:
        """Generate JWT token for user"""
        payload = {
            'user_id': user_id,
            'exp': datetime.utcnow() + timedelta(days=7),  # Token expires in 7 days
            'iat': datetime.utcnow()
        }
        
        secret_key = os.getenv('JWT_SECRET_KEY')
        return jwt.encode(payload, secret_key, algorithm='HS256')
    
    @staticmethod
    def decode_token(token: str) -> Optional[Dict]:
        """Decode JWT token and return payload"""
        try:
            secret_key = os.getenv('JWT_SECRET_KEY')
            payload = jwt.decode(token, secret_key, algorithms=['HS256'])
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None