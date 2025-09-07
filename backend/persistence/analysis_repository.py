from pymongo import MongoClient
from bson import ObjectId
from config.database import get_db
from models.analysis_model import VideoAnalysis, AutomationExecution
from typing import Optional, List, Dict, Any

class AnalysisRepository:
    def __init__(self):
        self.db = get_db()
        if self.db is None:
            raise Exception("Database not initialized. Please call init_db() first.")
        self.collection = self.db.video_analyses
    
    def create_analysis(self, analysis: VideoAnalysis) -> str:
        """Create a new video analysis record"""
        analysis_dict = analysis.to_dict()
        result = self.collection.insert_one(analysis_dict)
        return str(result.inserted_id)
    
    def find_analysis_by_video_id(self, video_id: str) -> Optional[Dict[str, Any]]:
        """Find analysis by video ID"""
        analysis = self.collection.find_one({'video_id': video_id})
        if analysis:
            analysis['_id'] = str(analysis['_id'])
        return analysis
    
    def find_analysis_by_id(self, analysis_id: str) -> Optional[Dict[str, Any]]:
        """Find analysis by ID"""
        try:
            analysis = self.collection.find_one({'_id': ObjectId(analysis_id)})
            if analysis:
                analysis['_id'] = str(analysis['_id'])
            return analysis
        except:
            return None
    
    def update_analysis(self, analysis_id: str, update_data: Dict[str, Any]) -> bool:
        """Update analysis record"""
        try:
            result = self.collection.update_one(
                {'_id': ObjectId(analysis_id)},
                {'$set': update_data}
            )
            return result.modified_count > 0
        except:
            return False

class ExecutionRepository:
    def __init__(self):
        self.db = get_db()
        if self.db is None:
            raise Exception("Database not initialized. Please call init_db() first.")
        self.collection = self.db.automation_executions
    
    def create_execution(self, execution: AutomationExecution) -> str:
        """Create a new automation execution record"""
        execution_dict = execution.to_dict()
        result = self.collection.insert_one(execution_dict)
        return str(result.inserted_id)
    
    def find_execution_by_video_id(self, video_id: str) -> Optional[Dict[str, Any]]:
        """Find execution by video ID"""
        execution = self.collection.find_one({'video_id': video_id})
        if execution:
            execution['_id'] = str(execution['_id'])
        return execution
    
    def find_execution_by_id(self, execution_id: str) -> Optional[Dict[str, Any]]:
        """Find execution by ID"""
        try:
            execution = self.collection.find_one({'_id': ObjectId(execution_id)})
            if execution:
                execution['_id'] = str(execution['_id'])
            return execution
        except:
            return None
    
    def find_executions_by_analysis_id(self, analysis_id: str) -> List[Dict[str, Any]]:
        """Find all executions for an analysis"""
        executions = list(self.collection.find({'analysis_id': analysis_id}))
        for execution in executions:
            execution['_id'] = str(execution['_id'])
        return executions
    
    def update_execution(self, execution_id: str, update_data: Dict[str, Any]) -> bool:
        """Update execution record"""
        try:
            result = self.collection.update_one(
                {'_id': ObjectId(execution_id)},
                {'$set': update_data}
            )
            return result.modified_count > 0
        except:
            return False