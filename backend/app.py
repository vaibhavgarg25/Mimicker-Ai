import os
from flask import Flask, jsonify
from flask_cors import CORS   # 👈 import here
from dotenv import load_dotenv
from config.database import init_db
from controllers.auth_controller import auth_bp
from controllers.video_controller import video_bp

# Load environment variables
load_dotenv()

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max file size
    
    # Enable CORS (allow frontend)
    CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})
    # Or allow all origins (less secure, but good for dev):
    # CORS(app)

    # Initialize database
    init_db()
    
    # Create uploads directory if it doesn't exist
    os.makedirs('uploads', exist_ok=True)
    
    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(video_bp, url_prefix='/api/videos')
    
    # Health check endpoint
    @app.route('/api/health', methods=['GET'])
    def health_check():
        return jsonify({
            'status': 'success',
            'message': 'Mimicker AI Backend is running'
        }), 200
    
    # Error handlers
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
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=8000)
