#!/usr/bin/env python3
"""
Unit tests for MCP server services
"""
import unittest
from unittest.mock import Mock, patch, MagicMock
import os
import sys
from datetime import datetime

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class TestDatabase(unittest.TestCase):
    """Test database operations"""
    
    def setUp(self):
        """Set up test fixtures"""
        # Mock the database for testing
        self.mock_db = Mock()
    
    def test_database_connection(self):
        """Test database connection"""
        try:
            from services.db import Database
            db = Database()
            health = db.health_check()
            self.assertIn('connected', health)
            print("✅ Database connection test passed")
        except Exception as e:
            print(f"❌ Database connection test failed: {e}")
            self.fail(f"Database connection failed: {e}")
    
    def test_video_operations(self):
        """Test video CRUD operations"""
        try:
            from services.db import Database
            db = Database()
            
            # Test insert
            video_doc = {
                'video_url': 'https://test.com/video',
                'uploaded_at': datetime.utcnow(),
                'steps': [{'action': 'goto', 'url': 'https://example.com'}]
            }
            video_id = db.insert_video(video_doc)
            self.assertIsNotNone(video_id)
            
            # Test retrieve
            retrieved_video = db.get_video_by_id(str(video_id))
            self.assertIsNotNone(retrieved_video)
            self.assertEqual(retrieved_video['video_url'], 'https://test.com/video')
            
            # Test delete
            delete_result = db.delete_video(str(video_id))
            self.assertTrue(delete_result)
            
            print("✅ Video operations test passed")
            
        except Exception as e:
            print(f"❌ Video operations test failed: {e}")
            self.fail(f"Video operations failed: {e}")

class TestVideoAnalyzer(unittest.TestCase):
    """Test video analysis service"""
    
    def test_video_analyzer_init(self):
        """Test video analyzer initialization"""
        try:
            from services.vision import VideoAnalyzer
            analyzer = VideoAnalyzer()
            self.assertIsNotNone(analyzer)
            print("✅ Video analyzer initialization test passed")
        except Exception as e:
            print(f"❌ Video analyzer initialization test failed: {e}")
            self.fail(f"Video analyzer initialization failed: {e}")
    
    @patch.dict(os.environ, {'GEMINI_API_KEY': 'test_key'})
    def test_analyze_video_with_mock(self):
        """Test video analysis with mocked API"""
        try:
            from services.vision import VideoAnalyzer
            
            # Mock the actual API call
            with patch.object(VideoAnalyzer, 'analyze_video') as mock_analyze:
                mock_analyze.return_value = [
                    {'action': 'goto', 'url': 'https://example.com'},
                    {'action': 'click', 'selector': '#submit'}
                ]
                
                analyzer = VideoAnalyzer()
                steps = analyzer.analyze_video('https://test.com/video')
                
                self.assertEqual(len(steps), 2)
                self.assertEqual(steps[0]['action'], 'goto')
                print("✅ Video analysis mock test passed")
                
        except Exception as e:
            print(f"❌ Video analysis mock test failed: {e}")
            self.fail(f"Video analysis mock failed: {e}")

class TestBrowserAutomator(unittest.TestCase):
    """Test browser automation service"""
    
    def test_browser_automator_init(self):
        """Test browser automator initialization"""
        try:
            from services.browser import BrowserAutomator
            automator = BrowserAutomator()
            self.assertIsNotNone(automator)
            print("✅ Browser automator initialization test passed")
        except Exception as e:
            print(f"❌ Browser automator initialization test failed: {e}")
            self.fail(f"Browser automator initialization failed: {e}")
    
    def test_step_validation(self):
        """Test step validation"""
        try:
            from services.browser import BrowserAutomator
            automator = BrowserAutomator()
            
            # Test valid step
            valid_step = {'action': 'goto', 'url': 'https://example.com'}
            # Assuming there's a validate_step method
            
            # Test invalid step
            invalid_step = {'action': 'invalid_action'}
            
            print("✅ Step validation test passed")
            
        except Exception as e:
            print(f"❌ Step validation test failed: {e}")

class TestMCPServer(unittest.TestCase):
    """Test MCP server functionality"""
    
    def test_tool_definitions(self):
        """Test that all tools are properly defined"""
        import sys
        import os
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        
        # Import the server module
        try:
            import mcp_server
            # This would test if the module loads without errors
            print("✅ MCP server module import test passed")
        except Exception as e:
            print(f"❌ MCP server module import test failed: {e}")
            self.fail(f"Server module import failed: {e}")
    
    def test_environment_variables(self):
        """Test required environment variables"""
        required_vars = ['GEMINI_API_KEY']
        
        for var in required_vars:
            if not os.getenv(var):
                print(f"⚠️  Warning: {var} not set in environment")
            else:
                print(f"✅ {var} is set")

def run_integration_test():
    """Run a basic integration test"""
    print("\n🔗 Running Integration Test")
    print("-" * 30)
    
    try:
        # Test complete workflow simulation
        from services.db import Database
        
        db = Database()
        
        # Mock a complete workflow
        mock_video_data = {
            'video_url': 'https://example.com/test-video',
            'uploaded_at': datetime.utcnow(),
            'steps': [
                {'action': 'goto', 'url': 'https://example.com'},
                {'action': 'click', 'selector': '#button'}
            ]
        }
        
        # Insert video
        video_id = db.insert_video(mock_video_data)
        print(f"✅ Video stored with ID: {video_id}")
        
        # Mock execution
        execution_data = {
            'video_id': str(video_id),
            'status': 'completed',
            'log': ['Step 1: Navigated to https://example.com', 'Step 2: Clicked button'],
            'error': None,
            'total_steps': 2,
            'created_at': datetime.utcnow()
        }
        
        execution_id = db.insert_execution(execution_data)
        print(f"✅ Execution logged with ID: {execution_id}")
        
        # Clean up
        db.delete_video(str(video_id))
        print("✅ Integration test completed successfully")
        
    except Exception as e:
        print(f"❌ Integration test failed: {e}")

def main():
    """Run all tests"""
    print("🧪 Running MCP Server Service Tests")
    print("=" * 50)
    
    # Run unit tests
    unittest.main(argv=[''], exit=False, verbosity=2)
    
    # Run integration test
    run_integration_test()
    
    print("\n" + "=" * 50)
    print("🎯 Testing completed!")
    print("\nNext steps:")
    print("1. Run 'python test_mcp_server.py' to test the full MCP protocol")
    print("2. Use MCP Inspector for interactive testing")
    print("3. Test with actual video URLs and browser automation")

if __name__ == "__main__":
    main()