from typing import Optional, Dict
from pymongo.errors import DuplicateKeyError
from config.database import get_db
from models.user_model import User
from bson import ObjectId

class UserRepository:
    def __init__(self):
        self.db = get_db()
        if self.db is None:
            raise Exception("Database not initialized. Please call init_db() first.")
        self.collection = self.db.users

    def _build_id_query(self, user_id: str) -> Dict:
        if getattr(self.db, "mode", None) == "local":
            return {'_id': user_id}
        return {'_id': ObjectId(user_id)}
    
    def create_user(self, user: User) -> Optional[str]:
        """Create a new user and return the user ID"""
        try:
            existing_user = self.find_user_by_email(user.email)
            if existing_user:
                raise ValueError("User with this email already exists")

            user_dict = user.to_dict()
            del user_dict['_id']  # Remove _id to let MongoDB generate it
            
            result = self.collection.insert_one(user_dict)
            return str(result.inserted_id)
        
        except DuplicateKeyError:
            raise ValueError("User with this email already exists")
        except Exception as e:
            raise Exception(f"Error creating user: {str(e)}")
    
    def find_user_by_email(self, email: str) -> Optional[Dict]:
        """Find user by email"""
        try:
            user = self.collection.find_one({'email': email})
            if user:
                user['_id'] = str(user['_id'])
            return user
        except Exception as e:
            raise Exception(f"Error finding user: {str(e)}")
    
    def find_user_by_id(self, user_id: str) -> Optional[Dict]:
        """Find user by ID"""
        try:
            user = self.collection.find_one(self._build_id_query(user_id))
            if user:
                user['_id'] = str(user['_id'])
            return user
        except Exception as e:
            raise Exception(f"Error finding user: {str(e)}")
