import os
from flask import Blueprint, request, jsonify, g
from middleware.auth_middleware import jwt_required
from services.mcp_client import MCPClient
from persistence.analysis_repository import AnalysisRepository, ExecutionRepository
from persistence.video_repository import VideoRepository
from models.analysis_model import VideoAnalysis, AutomationExecution
import threading
from datetime import datetime

automation_bp = Blueprint('automation', __name__)

# Initialize services
mcp_client = MCPClient()
analysis_repo = None
execution_repo = None
video_repo = None

def get_repositories():
    """Initialize repositories if needed"""
    global analysis_repo, execution_repo, video_repo
    if analysis_repo is None:
        analysis_repo = AnalysisRepository()
    if execution_repo is None:
        execution_repo = ExecutionRepository()
    if video_repo is None:
        video_repo = VideoRepository()
    return analysis_repo, execution_repo, video_repo

def process_video_async(video_id: str, video_path: str, user_id: str):
    """
    Asynchronous video processing function
    """
    try:
        print(f"🎬 Starting async processing for video {video_id}")
        
        # Initialize repositories
        analysis_repo, execution_repo, video_repo = get_repositories()
        
        # Step 1: Analyze video
        print("📊 Analyzing video...")
        analysis_result = mcp_client.analyze_video(video_path)
        
        if analysis_result['success']:
            data = analysis_result['data']
            steps = data.get('steps', [])
            
            # Save analysis to database
            analysis = VideoAnalysis(
                video_id=video_id,
                steps=steps,
                status='completed'
            )
            analysis_id = analysis_repo.create_analysis(analysis)
            print(f"✅ Analysis completed with {len(steps)} steps")
            
            # Step 2: Execute automation
            print("🤖 Starting automation...")
            execution = AutomationExecution(
                analysis_id=analysis_id,
                video_id=video_id,
                status='running'
            )
            execution_id = execution_repo.create_execution(execution)
            
            # Use the actual analyzed steps from the video
            if steps and len(steps) > 0:
                print(f"🎬 Executing browser automation with {len(steps)} steps extracted from video...")
                # Execute automation via MCP server with real video steps
                automation_result = mcp_client.execute_automation(steps, video_id)
            else:
                # Fallback: if no steps were extracted, show a simple demo
                fallback_steps = [
                    {
                        "action": "goto",
                        "url": "https://example.com",
                        "description": "Fallback demo - no steps extracted from video"
                    },
                    {
                        "action": "wait",
                        "timeout": 3000,
                        "description": "Video analysis did not extract actionable steps"
                    }
                ]
                print(f"⚠️ No steps extracted from video, using fallback demo with {len(fallback_steps)} steps...")
                automation_result = mcp_client.execute_automation(fallback_steps, video_id)
            
            if automation_result['success']:
                exec_data = automation_result['data']
                execution_repo.update_execution(execution_id, {
                    'status': 'completed',
                    'execution_id': exec_data.get('execution_id'),
                    'log': exec_data.get('log', []),
                    'updated_at': datetime.utcnow()
                })
                print("✅ Automation completed successfully")
            else:
                execution_repo.update_execution(execution_id, {
                    'status': 'failed',
                    'error': automation_result['error'],
                    'updated_at': datetime.utcnow()
                })
                print(f"❌ Automation failed: {automation_result['error']}")
        else:
            # Save failed analysis
            analysis = VideoAnalysis(
                video_id=video_id,
                steps=[],
                status='failed',
                error=analysis_result['error']
            )
            analysis_repo.create_analysis(analysis)
            print(f"❌ Analysis failed: {analysis_result['error']}")
            
    except Exception as e:
        print(f"❌ Async processing failed: {str(e)}")
        # Try to save error state
        try:
            analysis = VideoAnalysis(
                video_id=video_id,
                steps=[],
                status='failed',
                error=str(e)
            )
            analysis_repo.create_analysis(analysis)
        except:
            pass

@automation_bp.route('/trigger/<video_id>', methods=['POST'])
@jwt_required
def trigger_automation(video_id):
    """
    Trigger video analysis and automation for a specific video
    """
    try:
        # Initialize repositories
        analysis_repo, execution_repo, video_repo = get_repositories()
        
        # Verify video exists and belongs to user
        video = video_repo.find_video_by_id(video_id)
        if not video:
            return jsonify({
                'status': 'error',
                'message': 'Video not found'
            }), 404
        
        if video['user_id'] != g.current_user['_id']:
            return jsonify({
                'status': 'error',
                'message': 'Access denied'
            }), 403
        
        # Check if analysis already exists
        existing_analysis = analysis_repo.find_analysis_by_video_id(video_id)
        if existing_analysis:
            return jsonify({
                'status': 'success',
                'message': 'Analysis already exists',
                'data': {
                    'analysis_id': existing_analysis['_id'],
                    'status': existing_analysis['status']
                }
            }), 200
        
        # Check MCP server health
        if not mcp_client.health_check():
            return jsonify({
                'status': 'error',
                'message': 'MCP server is not available'
            }), 503
        
        # Get video file path
        video_path = os.path.join('uploads', video['filename'])
        if not os.path.exists(video_path):
            return jsonify({
                'status': 'error',
                'message': 'Video file not found'
            }), 404
        
        # Start async processing
        thread = threading.Thread(
            target=process_video_async,
            args=(video_id, video_path, g.current_user['_id'])
        )
        thread.daemon = True
        thread.start()
        
        return jsonify({
            'status': 'success',
            'message': 'Video processing started',
            'data': {
                'video_id': video_id,
                'status': 'processing'
            }
        }), 202
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'Failed to trigger automation'
        }), 500

@automation_bp.route('/status/<video_id>', methods=['GET'])
@jwt_required
def get_automation_status(video_id):
    """
    Get automation status for a video
    """
    try:
        # Initialize repositories
        analysis_repo, execution_repo, video_repo = get_repositories()
        
        # Verify video belongs to user
        video = video_repo.find_video_by_id(video_id)
        if not video or video['user_id'] != g.current_user['_id']:
            return jsonify({
                'status': 'error',
                'message': 'Video not found or access denied'
            }), 404
        
        # Get analysis
        analysis = analysis_repo.find_analysis_by_video_id(video_id)
        if not analysis:
            return jsonify({
                'status': 'success',
                'data': {
                    'video_id': video_id,
                    'analysis_status': 'not_started',
                    'execution_status': 'not_started'
                }
            }), 200
        
        # Get execution
        execution = execution_repo.find_execution_by_video_id(video_id)
        
        return jsonify({
            'status': 'success',
            'data': {
                'video_id': video_id,
                'analysis_status': analysis['status'],
                'analysis_steps': len(analysis.get('steps', [])),
                'analysis_error': analysis.get('error'),
                'execution_status': execution['status'] if execution else 'not_started',
                'execution_log': execution.get('log', []) if execution else [],
                'execution_error': execution.get('error') if execution else None,
                'last_updated': analysis['updated_at'].isoformat() if analysis.get('updated_at') else None
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'Failed to get automation status'
        }), 500

@automation_bp.route('/results/<video_id>', methods=['GET'])
@jwt_required
def get_automation_results(video_id):
    """
    Get detailed automation results for a video
    """
    try:
        # Initialize repositories
        analysis_repo, execution_repo, video_repo = get_repositories()
        
        # Verify video belongs to user
        video = video_repo.find_video_by_id(video_id)
        if not video or video['user_id'] != g.current_user['_id']:
            return jsonify({
                'status': 'error',
                'message': 'Video not found or access denied'
            }), 404
        
        # Get analysis and execution
        analysis = analysis_repo.find_analysis_by_video_id(video_id)
        execution = execution_repo.find_execution_by_video_id(video_id)
        
        if not analysis:
            return jsonify({
                'status': 'error',
                'message': 'No analysis found for this video'
            }), 404
        
        return jsonify({
            'status': 'success',
            'data': {
                'video': {
                    'id': video_id,
                    'filename': video['original_name'],
                    'upload_date': video['upload_timestamp'].isoformat()
                },
                'analysis': {
                    'id': analysis['_id'],
                    'status': analysis['status'],
                    'steps': analysis.get('steps', []),
                    'error': analysis.get('error'),
                    'created_at': analysis['created_at'].isoformat()
                },
                'execution': {
                    'id': execution['_id'] if execution else None,
                    'status': execution['status'] if execution else 'not_started',
                    'log': execution.get('log', []) if execution else [],
                    'error': execution.get('error') if execution else None,
                    'created_at': execution['created_at'].isoformat() if execution else None
                } if execution else None
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'Failed to get automation results'
        }), 500

@automation_bp.route('/health', methods=['GET'])
def automation_health():
    """
    Check automation service health
    """
    mcp_healthy = mcp_client.health_check()
    
    return jsonify({
        'status': 'success',
        'data': {
            'automation_service': 'healthy',
            'mcp_server': 'healthy' if mcp_healthy else 'unavailable',
            'timestamp': datetime.utcnow().isoformat()
        }
    }), 200