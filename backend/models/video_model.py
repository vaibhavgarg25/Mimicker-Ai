from datetime import datetime
from typing import Dict, Optional

class Video:
    def __init__(self, filename: str, user_id: str, original_name: str, 
                 file_size: int, _id: Optional[str] = None):
        self._id = _id
        self.filename = filename
        self.user_id = user_id
        self.original_name = original_name
        self.file_size = file_size
        self.upload_timestamp = datetime.utcnow()
        self.status = 'uploaded'  # uploaded, processing, completed, error
    
    def to_dict(self) -> Dict:
        return {
            '_id': str(self._id) if self._id else None,
            'filename': self.filename,
            'user_id': self.user_id,
            'original_name': self.original_name,
            'file_size': self.file_size,
            'upload_timestamp': self.upload_timestamp,
            'status': self.status
        }