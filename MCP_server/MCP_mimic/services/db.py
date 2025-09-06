# services/db.py - MongoDB Database Service
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime
import os
from typing import List, Dict, Any, Optional

class Database:
    def __init__(self):
        # MongoDB connection
        self.mongo_uri = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
        self.db_name = os.getenv('DB_NAME', 'browser_automation')
        
        self.client = MongoClient(self.mongo_uri)
        self.db = self.client[self.db_name]
        
        # Collections
        self.videos = self.db.videos
        self.executions = self.db.executions
        self.corrections = self.db.corrections
        
        # Create indexes for better performance
        self._create_indexes()
    
    def _create_indexes(self):
        """Create database indexes"""
        try:
            # Index on video_url for videos collection
            self.videos.create_index("video_url")
            self.videos.create_index("uploaded_at")
            
            # Index on video_id for executions collection
            self.executions.create_index("video_id")
            self.executions.create_index("created_at")
            
            # Index on execution_id for corrections collection
            self.corrections.create_index("execution_id")
            self.corrections.create_index("created_at")
            
        except Exception as e:
            print(f"Index creation warning: {e}")
    
    # Video CRUD operations
    def insert_video(self, video_doc: Dict[str, Any]) -> ObjectId:
        """Insert a new video document"""
        try:
            result = self.videos.insert_one(video_doc)
            return result.inserted_id
        except Exception as e:
            raise Exception(f"Failed to insert video: {str(e)}")
    
    def get_video_by_id(self, video_id: str) -> Optional[Dict[str, Any]]:
        """Get video document by ID"""
        try:
            video = self.videos.find_one({"_id": ObjectId(video_id)})
            if video:
                video['_id'] = str(video['_id'])
            return video
        except Exception as e:
            raise Exception(f"Failed to get video: {str(e)}")
    
    def get_all_videos(self) -> List[Dict[str, Any]]:
        """Get all video documents"""
        try:
            videos = list(self.videos.find().sort("uploaded_at", -1))
            for video in videos:
                video['_id'] = str(video['_id'])
            return videos
        except Exception as e:
            raise Exception(f"Failed to get videos: {str(e)}")
    
    def update_video(self, video_id: str, update_doc: Dict[str, Any]) -> bool:
        """Update video document"""
        try:
            result = self.videos.update_one(
                {"_id": ObjectId(video_id)},
                {"$set": update_doc}
            )
            return result.modified_count > 0
        except Exception as e:
            raise Exception(f"Failed to update video: {str(e)}")
    
    def delete_video(self, video_id: str) -> bool:
        """Delete video document"""
        try:
            result = self.videos.delete_one({"_id": ObjectId(video_id)})
            return result.deleted_count > 0
        except Exception as e:
            raise Exception(f"Failed to delete video: {str(e)}")
    
    def find_videos_by_url(self, video_url: str) -> List[Dict[str, Any]]:
        """Find videos by URL"""
        try:
            videos = list(self.videos.find({"video_url": video_url}))
            for video in videos:
                video['_id'] = str(video['_id'])
            return videos
        except Exception as e:
            raise Exception(f"Failed to find videos: {str(e)}")
    
    # Execution CRUD operations
    def insert_execution(self, execution_doc: Dict[str, Any]) -> ObjectId:
        """Insert a new execution document"""
        try:
            result = self.executions.insert_one(execution_doc)
            return result.inserted_id
        except Exception as e:
            raise Exception(f"Failed to insert execution: {str(e)}")
    
    def get_execution_by_id(self, execution_id: str) -> Optional[Dict[str, Any]]:
        """Get execution document by ID"""
        try:
            execution = self.executions.find_one({"_id": ObjectId(execution_id)})
            if execution:
                execution['_id'] = str(execution['_id'])
                if execution.get('video_id'):
                    execution['video_id'] = str(execution['video_id'])
            return execution
        except Exception as e:
            raise Exception(f"Failed to get execution: {str(e)}")
    
    def get_executions_by_video_id(self, video_id: str) -> List[Dict[str, Any]]:
        """Get all executions for a video"""
        try:
            executions = list(self.executions.find({"video_id": ObjectId(video_id)}).sort("created_at", -1))
            for execution in executions:
                execution['_id'] = str(execution['_id'])
                execution['video_id'] = str(execution['video_id'])
            return executions
        except Exception as e:
            raise Exception(f"Failed to get executions: {str(e)}")
    
    def get_all_executions(self) -> List[Dict[str, Any]]:
        """Get all execution documents"""
        try:
            executions = list(self.executions.find().sort("created_at", -1))
            for execution in executions:
                execution['_id'] = str(execution['_id'])
                if execution.get('video_id'):
                    execution['video_id'] = str(execution['video_id'])
            return executions
        except Exception as e:
            raise Exception(f"Failed to get executions: {str(e)}")
    
    def update_execution(self, execution_id: str, update_doc: Dict[str, Any]) -> bool:
        """Update execution document"""
        try:
            result = self.executions.update_one(
                {"_id": ObjectId(execution_id)},
                {"$set": update_doc}
            )
            return result.modified_count > 0
        except Exception as e:
            raise Exception(f"Failed to update execution: {str(e)}")
    
    # Correction CRUD operations
    def insert_correction(self, correction_doc: Dict[str, Any]) -> ObjectId:
        """Insert a new correction document"""
        try:
            result = self.corrections.insert_one(correction_doc)
            return result.inserted_id
        except Exception as e:
            raise Exception(f"Failed to insert correction: {str(e)}")
    
    def get_correction_by_id(self, correction_id: str) -> Optional[Dict[str, Any]]:
        """Get correction document by ID"""
        try:
            correction = self.corrections.find_one({"_id": ObjectId(correction_id)})
            if correction:
                correction['_id'] = str(correction['_id'])
                if correction.get('execution_id'):
                    correction['execution_id'] = str(correction['execution_id'])
            return correction
        except Exception as e:
            raise Exception(f"Failed to get correction: {str(e)}")
    
    def get_corrections_by_execution_id(self, execution_id: str) -> List[Dict[str, Any]]:
        """Get all corrections for an execution"""
        try:
            corrections = list(self.corrections.find({"execution_id": ObjectId(execution_id)}).sort("created_at", -1))
            for correction in corrections:
                correction['_id'] = str(correction['_id'])
                correction['execution_id'] = str(correction['execution_id'])
            return corrections
        except Exception as e:
            raise Exception(f"Failed to get corrections: {str(e)}")
    
    def get_all_corrections(self) -> List[Dict[str, Any]]:
        """Get all correction documents"""
        try:
            corrections = list(self.corrections.find().sort("created_at", -1))
            for correction in corrections:
                correction['_id'] = str(correction['_id'])
                if correction.get('execution_id'):
                    correction['execution_id'] = str(correction['execution_id'])
            return corrections
        except Exception as e:
            raise Exception(f"Failed to get corrections: {str(e)}")
    
    # Analytics and reporting methods
    def get_execution_stats(self) -> Dict[str, Any]:
        """Get execution statistics"""
        try:
            total_executions = self.executions.count_documents({})
            successful_executions = self.executions.count_documents({"status": "completed"})
            failed_executions = self.executions.count_documents({"status": "failed"})
            
            return {
                "total_executions": total_executions,
                "successful_executions": successful_executions,
                "failed_executions": failed_executions,
                "success_rate": (successful_executions / total_executions * 100) if total_executions > 0 else 0
            }
        except Exception as e:
            raise Exception(f"Failed to get execution stats: {str(e)}")
    
    def get_recent_activity(self, limit: int = 10) -> Dict[str, Any]:
        """Get recent activity across all collections"""
        try:
            recent_videos = list(self.videos.find().sort("uploaded_at", -1).limit(limit))
            recent_executions = list(self.executions.find().sort("created_at", -1).limit(limit))
            recent_corrections = list(self.corrections.find().sort("created_at", -1).limit(limit))
            
            # Convert ObjectIds to strings
            for video in recent_videos:
                video['_id'] = str(video['_id'])
            
            for execution in recent_executions:
                execution['_id'] = str(execution['_id'])
                if execution.get('video_id'):
                    execution['video_id'] = str(execution['video_id'])
            
            for correction in recent_corrections:
                correction['_id'] = str(correction['_id'])
                if correction.get('execution_id'):
                    correction['execution_id'] = str(correction['execution_id'])
            
            return {
                "recent_videos": recent_videos,
                "recent_executions": recent_executions,
                "recent_corrections": recent_corrections
            }
        except Exception as e:
            raise Exception(f"Failed to get recent activity: {str(e)}")
    
    def cleanup_old_data(self, days: int = 30) -> Dict[str, int]:
        """Clean up data older than specified days"""
        try:
            cutoff_date = datetime.utcnow() - timedelta(days=days)
            
            # Delete old executions
            executions_deleted = self.executions.delete_many(
                {"created_at": {"$lt": cutoff_date}}
            ).deleted_count
            
            # Delete old corrections
            corrections_deleted = self.corrections.delete_many(
                {"created_at": {"$lt": cutoff_date}}
            ).deleted_count
            
            # Optionally delete old videos (be careful with this)
            # videos_deleted = self.videos.delete_many(
            #     {"uploaded_at": {"$lt": cutoff_date}}
            # ).deleted_count
            
            return {
                "executions_deleted": executions_deleted,
                "corrections_deleted": corrections_deleted
            }
        except Exception as e:
            raise Exception(f"Failed to cleanup old data: {str(e)}")
    
    def close_connection(self):
        """Close database connection"""
        try:
            self.client.close()
        except Exception as e:
            print(f"Error closing database connection: {e}")
    
    def health_check(self) -> Dict[str, Any]:
        """Check database health and connectivity"""
        try:
            # Ping the database
            self.client.admin.command('ping')
            
            # Get collection stats
            videos_count = self.videos.count_documents({})
            executions_count = self.executions.count_documents({})
            corrections_count = self.corrections.count_documents({})
            
            return {
                "status": "healthy",
                "connected": True,
                "database": self.db_name,
                "collections": {
                    "videos": videos_count,
                    "executions": executions_count,
                    "corrections": corrections_count
                }
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "connected": False,
                "error": str(e)
            }