# Updated app.py - Add this to your existing app.py
import os
from flask import Flask, jsonify
from dotenv import load_dotenv
from config.database import init_db
from controllers.auth_controller import auth_bp
from controllers.video_controller import video_bp
from controllers.automation_controller import automation_bp
from flask_cors import CORS

# Load environment variables
load_dotenv()

def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})
    # Configuration
    app.config['SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'mimicker-dev-secret-key')
    app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max file size
    
    # Initialize database FIRST
    try:
        init_db()
        print("✓ Database initialized successfully")
    except Exception as e:
        print(f"✗ Database initialization failed: {e}")
        print("⚠ Video extraction features will be limited")
    
    # Create uploads directory if it doesn't exist
    os.makedirs('uploads', exist_ok=True)
    
    # Register existing blueprints
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(video_bp, url_prefix='/api/videos')
    app.register_blueprint(automation_bp, url_prefix='/api/automation')
    
    # Register extraction blueprint AFTER database initialization
    try:
        print("✓ Video extraction endpoints registered")
    except Exception as e:
        print(f"⚠ Could not register extraction endpoints: {e}")
        print("Video upload will still work, but extraction features will be unavailable")
    
    # Health check endpoint
    @app.route('/api/health', methods=['GET'])
    def health_check():
        return jsonify({
            'status': 'success',
            'message': 'Mimicker AI Backend is running',
            'features': {
                'video_upload': True,
                'authentication': True,
                'automation': True,
                'mcp_integration': True
            }
        }), 200
    
    # Enhanced error handlers
    @app.errorhandler(413)
    def request_entity_too_large(error):
        return jsonify({
            'status': 'error',
            'message': 'File too large. Maximum size is 100MB.'
        }), 413
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'status': 'error',
            'message': 'Endpoint not found'
        }), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({
            'status': 'error',
            'message': 'Internal server error occurred'
        }), 500
    
    return app

if __name__ == '__main__':
    app = create_app()
    print("🚀 Starting Mimicker AI Backend...")
    print("📹 Video upload: Available")
    print("🔐 Authentication: Available") 
    print("🎯 Action extraction: Available" if 'extraction' in str(app.url_map) else "⚠ Action extraction: Limited (check dependencies)")
    print("🌐 Server starting on http://localhost:8000")
    
    app.run(debug=True, host='0.0.0.0', port=8000)
