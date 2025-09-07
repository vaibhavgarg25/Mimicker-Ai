import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

client = None
db = None

def init_db():
    global client, db
    try:
        mongodb_uri = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/mimicker_ai')
        client = MongoClient(mongodb_uri)
        
        # Extract database name from URI or use default
        if 'mimicker_ai' in mongodb_uri:
            db_name = 'mimicker_ai'
        else:
            db_name = 'mimicker_ai'
        
        db = client[db_name]
        
        # Test connection
        client.admin.command('ping')
        print(f"✓ Connected to MongoDB successfully (database: {db_name})")
        
        # Create indexes
        try:
            db.users.create_index("email", unique=True)
            print("✓ Database indexes created")
        except Exception as idx_error:
            print(f"⚠ Index creation warning: {idx_error}")
        
    except Exception as e:
        print(f"✗ Error connecting to MongoDB: {e}")
        raise e

def get_db():
    return db