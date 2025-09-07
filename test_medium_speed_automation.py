#!/usr/bin/env python3
"""
Test the medium-speed human-like automation
"""

import requests
import json
import time

MCP_SERVER_URL = "http://localhost:8080"

def test_medium_speed():
    """Test medium-speed human-like automation"""
    print("🧪 Testing medium-speed human-like automation...")
    
    # Test steps with realistic timing
    test_steps = [
        {
            "action": "goto",
            "url": "https://www.google.com",
            "description": "Navigate to Google"
        },
        {
            "action": "wait",
            "timeout": 2000,
            "description": "Wait for page to load"
        },
        {
            "action": "type",
            "selector": "textarea[name='q']",
            "text": "YouTube automation test",
            "description": "Type search query with human-like speed"
        },
        {
            "action": "wait",
            "timeout": 1000,
            "description": "Wait after typing"
        },
        {
            "action": "click",
            "selector": "input[name='btnK']",
            "description": "Click search button with hover"
        },
        {
            "action": "wait",
            "timeout": 3000,
            "description": "Wait for search results"
        },
        {
            "action": "click",
            "selector": "h3 a",
            "description": "Click first result with human-like behavior"
        }
    ]
    
    try:
        payload = {
            'steps': test_steps,
            'video_id': 'medium_speed_test'
        }
        
        print("🎬 Running medium-speed test...")
        print("⏱️ Expected duration: ~15-20 seconds")
        
        start_time = time.time()
        
        response = requests.post(
            f"{MCP_SERVER_URL}/execute_browser_action",
            json=payload,
            timeout=60
        )
        
        end_time = time.time()
        duration = end_time - start_time
        
        if response.status_code == 200:
            data = response.json()
            success = data.get('success', False)
            log = data.get('log', [])
            
            print(f"🎬 Test {'PASSED' if success else 'FAILED'}!")
            print(f"⏱️ Duration: {duration:.1f} seconds")
            
            if log:
                print("\n📋 Actions performed:")
                for entry in log:
                    if "✓" in entry:
                        print(f"   ✅ {entry}")
                    elif "⚠️" in entry:
                        print(f"   ⚠️ {entry}")
            
            # Evaluate speed
            if duration < 10:
                print("\n⚡ Speed: FAST - Good for efficiency, may trigger CAPTCHAs")
            elif duration < 20:
                print("\n🎯 Speed: MEDIUM - Perfect balance of speed and human-like behavior")
            else:
                print("\n🐌 Speed: SLOW - Very human-like but may be too slow")
            
            return success
        else:
            print(f"❌ Test failed: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Test error: {e}")
        return False

def check_mcp_server():
    """Check if MCP server is running"""
    try:
        response = requests.get(f"{MCP_SERVER_URL}/health", timeout=5)
        return response.status_code == 200
    except:
        return False

def main():
    """Main test function"""
    print("🎯 MEDIUM-SPEED HUMAN-LIKE AUTOMATION TEST")
    print("=" * 45)
    
    # Check MCP server
    if not check_mcp_server():
        print("❌ MCP server is not running!")
        print("💡 Start it with: cd MCP_server/MCP_mimic && python main.py")
        return False
    
    print("✅ MCP server is running")
    print()
    
    # Run test
    success = test_medium_speed()
    
    if success:
        print("\n🎉 SUCCESS! Medium-speed automation is working!")
        print("\n🎬 The automation should now:")
        print("   ✅ Be fast enough to be efficient")
        print("   ✅ Be slow enough to avoid CAPTCHAs")
        print("   ✅ Include human-like behaviors (hover, natural typing)")
        print("   ✅ Have realistic delays between actions")
        
        print(f"\n🧪 Ready to test with your video!")
        choice = input("Test with your latest video? (y/n): ").strip().lower()
        
        if choice.startswith('y'):
            print("🎬 Run: python auto_run_latest_video.py")
    else:
        print("\n❌ Test failed - check the logs above")
    
    return success

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n⏹️ Test interrupted by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")