import requests
import json

def test_mcp_server():
    """Test if MCP server is running and working"""
    try:
        # Test health endpoint
        response = requests.get("http://localhost:3000/health", timeout=5)
        if response.status_code == 200:
            print("✅ MCP Server is running and healthy!")
            
            # Test video analysis
            test_payload = {"video_url": "test-video.mp4"}
            analysis_response = requests.post(
                "http://localhost:3000/analyze_video", 
                json=test_payload, 
                timeout=30
            )
            
            if analysis_response.status_code == 200:
                data = analysis_response.json()
                steps = data.get('steps', [])
                print(f"✅ Video analysis working! Extracted {len(steps)} steps")
                print(f"   Sample step: {steps[0] if steps else 'None'}")
                return True
            else:
                print(f"❌ Video analysis failed: {analysis_response.status_code}")
                return False
        else:
            print(f"❌ MCP Server health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ MCP Server not accessible: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Quick MCP Server Test")
    test_mcp_server()