from typing import Optional, List, Dict
from config.database import get_db
from models.video_model import Video
from bson import ObjectId

class VideoRepository:
    def __init__(self):
        self.db = get_db()
        if self.db is None:
            raise Exception("Database not initialized. Please call init_db() first.")
        self.collection = self.db.videos

    def _build_id_query(self, video_id: str) -> Dict:
        if getattr(self.db, "mode", None) == "local":
            return {'_id': video_id}
        return {'_id': ObjectId(video_id)}
    
    def create_video(self, video: Video) -> Optional[str]:
        """Save video metadata and return the video ID"""
        try:
            video_dict = video.to_dict()
            del video_dict['_id']  # Remove _id to let MongoDB generate it
            
            result = self.collection.insert_one(video_dict)
            return str(result.inserted_id)
        
        except Exception as e:
            raise Exception(f"Error saving video metadata: {str(e)}")
    
    def find_videos_by_user(self, user_id: str) -> List[Dict]:
        """Get all videos for a specific user"""
        try:
            videos = list(self.collection.find({'user_id': user_id}))
            for video in videos:
                video['_id'] = str(video['_id'])
            return videos
        except Exception as e:
            raise Exception(f"Error retrieving videos: {str(e)}")
    
    def find_video_by_id(self, video_id: str) -> Optional[Dict]:
        """Find video by ID"""
        try:
            video = self.collection.find_one(self._build_id_query(video_id))
            if video:
                video['_id'] = str(video['_id'])
            return video
        except Exception as e:
            raise Exception(f"Error finding video: {str(e)}")

    def update_video(self, video_id: str, update_data: Dict) -> bool:
        """Update video metadata"""
        try:
            result = self.collection.update_one(
                self._build_id_query(video_id),
                {'$set': update_data}
            )
            return result.modified_count > 0
        except Exception as e:
            raise Exception(f"Error updating video metadata: {str(e)}")
