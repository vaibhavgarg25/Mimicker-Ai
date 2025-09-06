# app.py - Main Flask Application
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
from services.vision import VideoAnalyzer
from services.browser import BrowserAutomator
from services.db import Database
from datetime import datetime
import traceback

load_dotenv()

app = Flask(__name__)
CORS(app)

# Initialize services
db = Database()
video_analyzer = VideoAnalyzer()
browser_automator = BrowserAutomator()

@app.route('/analyze_video', methods=['POST'])
def analyze_video():
    """
    Analyze a tutorial video and extract structured actions
    """
    try:
        data = request.get_json()
        video_url = data.get('video_url')
        
        if not video_url:
            return jsonify({'error': 'video_url is required'}), 400
        
        # Analyze video with Gemini
        steps = video_analyzer.analyze_video(video_url)
        
        # Store in database
        video_doc = {
            'video_url': video_url,
            'uploaded_at': datetime.utcnow(),
            'steps': steps
        }
        video_id = db.insert_video(video_doc)
        
        return jsonify({
            'video_id': str(video_id),
            'steps': steps
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/execute_browser_action', methods=['POST'])
def execute_browser_action():
    """
    Execute browser automation steps
    """
    try:
        data = request.get_json()
        steps = data.get('steps')
        video_id = data.get('video_id')
        
        if not steps:
            return jsonify({'error': 'steps are required'}), 400
        
        # Execute automation
        result = browser_automator.execute_steps(steps)
        
        # Log execution
        execution_doc = {
            'video_id': video_id,
            'status': 'completed' if result['success'] else 'failed',
            'log': result.get('log', []),
            'error': result.get('error'),
            'created_at': datetime.utcnow()
        }
        execution_id = db.insert_execution(execution_doc)
        
        return jsonify({
            'execution_id': str(execution_id),
            'success': result['success'],
            'log': result.get('log', []),
            'error': result.get('error')
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/fallback_llm', methods=['POST'])
def fallback_llm():
    """
    Get LLM suggestions for failed actions
    """
    try:
        data = request.get_json()
        error = data.get('error')
        context = data.get('context', {})
        
        if not error:
            return jsonify({'error': 'error message is required'}), 400
        
        # Get suggestion from Gemini
        suggestion = video_analyzer.suggest_correction(error, context)
        
        # Store correction
        correction_doc = {
            'execution_id': context.get('execution_id'),
            'error': error,
            'suggestion': suggestion,
            'created_at': datetime.utcnow()
        }
        db.insert_correction(correction_doc)
        
        return jsonify({'suggestion': suggestion})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/run_task_from_video', methods=['POST'])
def run_task_from_video():
    """
    Complete workflow: analyze video -> execute -> handle errors
    """
    try:
        data = request.get_json()
        video_url = data.get('video_url')
        
        if not video_url:
            return jsonify({'error': 'video_url is required'}), 400
        
        # Step 1: Analyze video
        steps = video_analyzer.analyze_video(video_url)
        
        # Store video
        video_doc = {
            'video_url': video_url,
            'uploaded_at': datetime.utcnow(),
            'steps': steps
        }
        video_id = db.insert_video(video_doc)
        
        # Step 2: Execute automation
        result = browser_automator.execute_steps(steps)
        
        # Step 3: Handle failures with LLM fallback
        if not result['success'] and result.get('error'):
            suggestion = video_analyzer.suggest_correction(
                result['error'], 
                {'steps': steps, 'video_url': video_url}
            )
            result['suggestion'] = suggestion
        
        # Log execution
        execution_doc = {
            'video_id': video_id,
            'status': 'completed' if result['success'] else 'failed',
            'log': result.get('log', []),
            'error': result.get('error'),
            'created_at': datetime.utcnow()
        }
        execution_id = db.insert_execution(execution_doc)
        
        return jsonify({
            'video_id': str(video_id),
            'execution_id': str(execution_id),
            'status': 'completed' if result['success'] else 'failed',
            'log': result.get('log', []),
            'error': result.get('error'),
            'suggestion': result.get('suggestion')
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# CRUD endpoints for tasks
@app.route('/tasks', methods=['GET'])
def get_tasks():
    """Get all tasks/videos"""
    try:
        tasks = db.get_all_videos()
        return jsonify({'tasks': tasks})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/tasks/<task_id>', methods=['GET'])
def get_task(task_id):
    """Get specific task by ID"""
    try:
        task = db.get_video_by_id(task_id)
        if not task:
            return jsonify({'error': 'Task not found'}), 404
        return jsonify({'task': task})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/tasks/<task_id>', methods=['DELETE'])
def delete_task(task_id):
    """Delete task by ID"""
    try:
        result = db.delete_video(task_id)
        if not result:
            return jsonify({'error': 'Task not found'}), 404
        return jsonify({'message': 'Task deleted successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/executions/<execution_id>', methods=['GET'])
def get_execution(execution_id):
    """Get execution details"""
    try:
        execution = db.get_execution_by_id(execution_id)
        if not execution:
            return jsonify({'error': 'Execution not found'}), 404
        return jsonify({'execution': execution})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.utcnow().isoformat()})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3000)