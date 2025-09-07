from datetime import datetime
from typing import Optional, List, Dict, Any

class VideoAnalysis:
    def __init__(self, video_id: str, steps: List[Dict[str, Any]], 
                 status: str = 'completed', error: Optional[str] = None, 
                 _id: Optional[str] = None):
        self._id = _id
        self.video_id = video_id
        self.steps = steps
        self.status = status  # 'pending', 'completed', 'failed'
        self.error = error
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
    
    def to_dict(self):
        result = {
            'video_id': self.video_id,
            'steps': self.steps,
            'status': self.status,
            'error': self.error,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
        # Only include _id if it's not None
        if self._id is not None:
            result['_id'] = self._id
        return result

class AutomationExecution:
    def __init__(self, analysis_id: str, video_id: str, status: str = 'pending',
                 log: Optional[List[str]] = None, error: Optional[str] = None,
                 execution_id: Optional[str] = None, _id: Optional[str] = None):
        self._id = _id
        self.analysis_id = analysis_id
        self.video_id = video_id
        self.execution_id = execution_id  # ID from MCP server
        self.status = status  # 'pending', 'running', 'completed', 'failed'
        self.log = log or []
        self.error = error
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
    
    def to_dict(self):
        result = {
            'analysis_id': self.analysis_id,
            'video_id': self.video_id,
            'execution_id': self.execution_id,
            'status': self.status,
            'log': self.log,
            'error': self.error,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
        # Only include _id if it's not None
        if self._id is not None:
            result['_id'] = self._id
        return result