#!/usr/bin/env python3
"""
Fix database issues for project review
"""

import sys
import os
sys.path.append('backend')

from config.database import get_db, init_db
from pymongo.errors import DuplicateKeyError

def fix_database():
    """Fix database issues"""
    print("🔧 Fixing Database Issues")
    
    try:
        # Initialize database
        init_db()
        db = get_db()
        
        if db is None:
            print("❌ Could not connect to database")
            return False
        
        print("✅ Connected to database")
        
        # Clean up any null _id entries in video_analyses
        print("\n📋 Cleaning up video_analyses collection...")
        
        # Remove any documents with null _id
        result = db.video_analyses.delete_many({"_id": None})
        print(f"   Removed {result.deleted_count} documents with null _id")
        
        # Remove any documents with empty _id
        result = db.video_analyses.delete_many({"_id": ""})
        print(f"   Removed {result.deleted_count} documents with empty _id")
        
        # Clean up automation_executions collection
        print("\n📋 Cleaning up automation_executions collection...")
        
        result = db.automation_executions.delete_many({"_id": None})
        print(f"   Removed {result.deleted_count} documents with null _id")
        
        result = db.automation_executions.delete_many({"_id": ""})
        print(f"   Removed {result.deleted_count} documents with empty _id")
        
        # Check collections
        print(f"\n📊 Collection Status:")
        print(f"   video_analyses: {db.video_analyses.count_documents({})} documents")
        print(f"   automation_executions: {db.automation_executions.count_documents({})} documents")
        print(f"   videos: {db.videos.count_documents({})} documents")
        print(f"   users: {db.users.count_documents({})} documents")
        
        print(f"\n✅ Database cleanup completed!")
        return True
        
    except Exception as e:
        print(f"❌ Database fix failed: {e}")
        return False

def test_database_operations():
    """Test database operations"""
    print("\n🧪 Testing Database Operations")
    
    try:
        db = get_db()
        
        # Test video_analyses insert
        test_analysis = {
            'video_id': 'test-video-123',
            'steps': [{'action': 'click', 'selector': 'button'}],
            'status': 'completed'
        }
        
        result = db.video_analyses.insert_one(test_analysis)
        print(f"✅ Test analysis inserted: {result.inserted_id}")
        
        # Clean up test data
        db.video_analyses.delete_one({'_id': result.inserted_id})
        print(f"✅ Test analysis cleaned up")
        
        return True
        
    except Exception as e:
        print(f"❌ Database test failed: {e}")
        return False

if __name__ == "__main__":
    success = fix_database()
    if success:
        test_success = test_database_operations()
        if test_success:
            print(f"\n🎉 Database is ready for project review!")
        else:
            print(f"\n⚠️ Database needs manual attention")
    else:
        print(f"\n❌ Database fix failed - manual intervention needed")