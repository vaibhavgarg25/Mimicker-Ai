import os
import uuid
from flask import Blueprint, request, jsonify, g
from werkzeug.utils import secure_filename
from middleware.auth_middleware import jwt_required
from persistence.video_repository import VideoRepository
from models.video_model import Video

video_bp = Blueprint('video', __name__)

ALLOWED_EXTENSIONS = {'mp4', 'mov', 'avi', 'mkv'}
UPLOAD_FOLDER = 'uploads'

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@video_bp.route('/upload', methods=['POST'])
@jwt_required
def upload_video():
    try:
        # Check if file is present in request
        if 'video' not in request.files:
            return jsonify({
                'status': 'error',
                'message': 'No video file provided'
            }), 400
        
        file = request.files['video']
        
        # Check if file is selected
        if file.filename == '':
            return jsonify({
                'status': 'error',
                'message': 'No video file selected'
            }), 400
        
        # Check file extension
        if not allowed_file(file.filename):
            return jsonify({
                'status': 'error',
                'message': 'Invalid file type. Allowed types: mp4, mov, avi, mkv'
            }), 400
        
        # Generate unique filename
        original_filename = file.filename
        file_extension = original_filename.rsplit('.', 1)[1].lower()
        unique_filename = f"{uuid.uuid4().hex}.{file_extension}"
        
        # Save file to uploads folder
        file_path = os.path.join(UPLOAD_FOLDER, unique_filename)
        file.save(file_path)
        
        # Get file size
        file_size = os.path.getsize(file_path)
        
        # Save video metadata to database
        video = Video(
            filename=unique_filename,
            user_id=g.current_user['_id'],
            original_name=original_filename,
            file_size=file_size
        )
        
        video_repo = VideoRepository()
        video_id = video_repo.create_video(video)
        
        return jsonify({
            'status': 'success',
            'message': 'Video uploaded successfully',
            'data': {
                'video_id': video_id,
                'filename': unique_filename,
                'original_name': original_filename,
                'file_size': file_size,
                'upload_timestamp': video.upload_timestamp.isoformat()
            }
        }), 201
    
    except Exception as e:
        # Clean up file if it was saved but database operation failed
        if 'file_path' in locals() and os.path.exists(file_path):
            os.remove(file_path)
        
        return jsonify({
            'status': 'error',
            'message': 'An error occurred during video upload'
        }), 500

@video_bp.route('/my-videos', methods=['GET'])
@jwt_required
def get_user_videos():
    try:
        video_repo = VideoRepository()
        videos = video_repo.find_videos_by_user(g.current_user['_id'])
        
        return jsonify({
            'status': 'success',
            'message': 'Videos retrieved successfully',
            'data': {
                'videos': videos,
                'count': len(videos)
            }
        }), 200
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'An error occurred while retrieving videos'
        }), 500

@video_bp.route('/<video_id>', methods=['GET'])
@jwt_required
def get_video_details(video_id):
    try:
        video_repo = VideoRepository()
        video = video_repo.find_video_by_id(video_id)
        
        if not video:
            return jsonify({
                'status': 'error',
                'message': 'Video not found'
            }), 404
        
        # Check if user owns the video
        if video['user_id'] != g.current_user['_id']:
            return jsonify({
                'status': 'error',
                'message': 'Access denied'
            }), 403
        
        return jsonify({
            'status': 'success',
            'message': 'Video details retrieved successfully',
            'data': {
                'video': video
            }
        }), 200
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'An error occurred while retrieving video details'
        }), 500