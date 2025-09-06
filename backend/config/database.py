import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

client = None
db = None

def init_db():
    global client, db
    try:
        mongodb_uri = os.getenv('MONGODB_URI')
        client = MongoClient(mongodb_uri)
        db = client.get_database()
        
        # Test connection
        client.admin.command('ping')
        print("✓ Connected to MongoDB successfully")
        
        # Create indexes
        db.users.create_index("email", unique=True)
        print("✓ Database indexes created")
        
    except Exception as e:
        print(f"✗ Error connecting to MongoDB: {e}")
        raise e

def get_db():
    return db