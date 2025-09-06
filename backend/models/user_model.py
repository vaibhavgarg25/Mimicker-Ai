from datetime import datetime
from typing import Dict, Optional

class User:
    def __init__(self, name: str, email: str, password_hash: str, _id: Optional[str] = None):
        self._id = _id
        self.name = name
        self.email = email
        self.password_hash = password_hash
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
    
    def to_dict(self) -> Dict:
        return {
            '_id': str(self._id) if self._id else None,
            'name': self.name,
            'email': self.email,
            'password_hash': self.password_hash,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
    
    def to_public_dict(self) -> Dict:
        """Return user data without sensitive information"""
        return {
            '_id': str(self._id) if self._id else None,
            'name': self.name,
            'email': self.email,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
