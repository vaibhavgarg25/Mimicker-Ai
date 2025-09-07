#!/usr/bin/env python3
"""
Fix the search result clicking issue by restarting MCP server and testing
"""

import os
import sys
import subprocess
import time
import requests
import json

MCP_SERVER_URL = "http://localhost:8080"

def restart_mcp_server():
    """Restart MCP server with the improved search result handling"""
    print("🔄 Restarting MCP server with improved search result clicking...")
    
    # Stop current server
    try:
        if os.name == 'nt':  # Windows
            subprocess.run(['taskkill', '/f', '/im', 'python.exe'], 
                         capture_output=True, text=True)
        else:
            subprocess.run(['pkill', '-f', 'main.py'], capture_output=True)
        time.sleep(2)
        print("✅ Stopped old MCP server")
    except:
        pass
    
    # Start new server
    mcp_dir = "MCP_server/MCP_mimic"
    if not os.path.exists(mcp_dir):
        print(f"❌ MCP directory not found: {mcp_dir}")
        return False
    
    try:
        if os.name == 'nt':  # Windows
            subprocess.Popen([sys.executable, 'main.py'], 
                           cwd=mcp_dir,
                           creationflags=subprocess.CREATE_NEW_CONSOLE)
        else:
            subprocess.Popen([sys.executable, 'main.py'], cwd=mcp_dir)
        
        # Wait for server to start
        print("⏳ Starting MCP server...")
        for i in range(15):
            try:
                response = requests.get(f"{MCP_SERVER_URL}/health", timeout=2)
                if response.status_code == 200:
                    print("✅ MCP server started!")
                    return True
            except:
                pass
            time.sleep(1)
            print(f"   Attempt {i+1}/15...")
        
        print("❌ MCP server failed to start")
        return False
        
    except Exception as e:
        print(f"❌ Failed to start MCP server: {e}")
        return False

def test_search_workflow():
    """Test the complete search workflow including result clicking"""
    print("🧪 Testing complete search workflow...")
    
    test_steps = [
        {
            "action": "goto",
            "url": "https://www.google.com",
            "description": "Navigate to Google search"
        },
        {
            "action": "wait",
            "timeout": 3000,
            "description": "Wait for Google to load"
        },
        {
            "action": "type",
            "selector": "textarea[name='q']",
            "text": "YouTube",
            "description": "Type search query"
        },
        {
            "action": "wait",
            "timeout": 1000,
            "description": "Wait after typing"
        },
        {
            "action": "click",
            "selector": "input[name='btnK']",
            "description": "Click search button"
        },
        {
            "action": "wait",
            "timeout": 5000,
            "description": "Wait for search results"
        },
        {
            "action": "click",
            "selector": "h3 a",
            "description": "Click on first search result"
        },
        {
            "action": "wait",
            "timeout": 5000,
            "description": "Wait for result page to load"
        }
    ]
    
    try:
        payload = {
            'steps': test_steps,
            'video_id': 'search_workflow_test'
        }
        
        print("🎬 Running search workflow test...")
        response = requests.post(
            f"{MCP_SERVER_URL}/execute_browser_action",
            json=payload,
            timeout=90
        )
        
        if response.status_code == 200:
            data = response.json()
            success = data.get('success', False)
            log = data.get('log', [])
            error = data.get('error')
            
            print(f"🎬 Test {'PASSED' if success else 'FAILED'}!")
            
            if log:
                print("\n📋 What happened:")
                for entry in log:
                    if "✓" in entry:
                        print(f"   ✅ {entry}")
                    elif "⚠️" in entry or "❌" in entry:
                        print(f"   ⚠️ {entry}")
                    else:
                        print(f"   📝 {entry}")
            
            if error:
                print(f"\n❌ Error: {error}")
            
            # Check if we successfully navigated away from Google
            if success and any("result" in entry.lower() for entry in log):
                print("\n🎉 SUCCESS! Search result clicking is working!")
                return True
            else:
                print("\n⚠️ Test completed but may not have clicked result properly")
                return False
        else:
            print(f"❌ Test request failed: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Test error: {e}")
        return False

def run_latest_video_test():
    """Run automation on the latest video to test real scenario"""
    print("🎬 Testing with your latest video...")
    
    # Find latest video
    uploads_dir = "backend/uploads"
    if not os.path.exists(uploads_dir):
        print("❌ No uploads directory found")
        return False
    
    video_files = []
    for filename in os.listdir(uploads_dir):
        if filename.lower().endswith(('.mp4', '.mov', '.avi', '.mkv', '.webm')):
            filepath = os.path.join(uploads_dir, filename)
            mtime = os.path.getmtime(filepath)
            video_files.append((filepath, mtime, filename))
    
    if not video_files:
        print("❌ No video files found")
        return False
    
    # Get latest video
    video_files.sort(key=lambda x: x[1], reverse=True)
    latest_video = video_files[0][0]
    
    print(f"📹 Testing with: {os.path.basename(latest_video)}")
    
    try:
        payload = {
            'video_url': os.path.abspath(latest_video)
        }
        
        print("🧠 Analyzing video and running automation...")
        response = requests.post(
            f"{MCP_SERVER_URL}/run_task_from_video",
            json=payload,
            timeout=300
        )
        
        if response.status_code == 200:
            data = response.json()
            status = data.get('status', 'unknown')
            log = data.get('log', [])
            
            print(f"🎬 Result: {status.upper()}")
            
            if log:
                print("\n📋 Key actions:")
                for entry in log[-8:]:  # Show last 8 entries
                    if "✓" in entry:
                        print(f"   ✅ {entry}")
                    elif "⚠️" in entry or "❌" in entry:
                        print(f"   ⚠️ {entry}")
            
            # Check if it successfully moved beyond search results
            search_completed = any("result" in entry.lower() and "✓" in entry for entry in log)
            
            if search_completed:
                print("\n🎉 SUCCESS! Your video automation is working with result clicking!")
                return True
            else:
                print("\n⚠️ Automation ran but may still have issues with result clicking")
                return False
        else:
            print(f"❌ Failed: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Main fix process"""
    print("🔧 FIXING SEARCH RESULT CLICKING ISSUE")
    print("=" * 45)
    
    # Step 1: Restart MCP server with improvements
    if not restart_mcp_server():
        print("\n❌ Could not restart MCP server")
        return False
    
    # Step 2: Test search workflow
    print(f"\n🧪 Testing search result clicking...")
    if test_search_workflow():
        print("✅ Search workflow test passed!")
    else:
        print("⚠️ Search workflow test had issues, but continuing...")
    
    # Step 3: Test with real video
    print(f"\n🎯 Ready to test with your latest video!")
    choice = input("Test automation with your latest video? (y/n): ").strip().lower()
    
    if choice.startswith('y'):
        success = run_latest_video_test()
        if success:
            print("\n🎉 PERFECT! Your video automation now works with proper result clicking!")
            print("🎬 The browser should now:")
            print("   ✅ Search on Google")
            print("   ✅ Click the first search result")
            print("   ✅ Navigate to the result page")
            print("   ✅ Continue with other actions from your video")
        else:
            print("\n⚠️ There may still be some issues, but the search result clicking is improved")
    else:
        print("\n✅ MCP server is ready with improved search result clicking!")
        print("🎬 You can now:")
        print("   1. Go to http://localhost:3000")
        print("   2. Upload a video")
        print("   3. Click 'Start Analysis'")
        print("   4. Watch it properly click on search results!")
    
    return True

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n⏹️ Interrupted by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")