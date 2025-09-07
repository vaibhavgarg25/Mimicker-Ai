#!/usr/bin/env python3
"""
Restart MCP server with improved browser automation
"""

import os
import sys
import subprocess
import time
import requests
import signal

def stop_mcp_server():
    """Stop any running MCP server processes"""
    print("🛑 Stopping MCP server...")
    
    try:
        # Try to find and kill MCP server process
        if os.name == 'nt':  # Windows
            subprocess.run(['taskkill', '/f', '/im', 'python.exe'], 
                         capture_output=True, text=True)
        else:  # Unix/Linux/Mac
            subprocess.run(['pkill', '-f', 'main.py'], 
                         capture_output=True, text=True)
        
        time.sleep(2)
        print("✅ MCP server stopped")
        return True
    except Exception as e:
        print(f"⚠️ Could not stop MCP server: {e}")
        return False

def start_mcp_server():
    """Start MCP server"""
    print("🚀 Starting MCP server...")
    
    mcp_dir = "MCP_server/MCP_mimic"
    if not os.path.exists(mcp_dir):
        print(f"❌ MCP directory not found: {mcp_dir}")
        return False
    
    try:
        # Change to MCP directory and start server
        os.chdir(mcp_dir)
        
        # Start server in background
        if os.name == 'nt':  # Windows
            subprocess.Popen([sys.executable, 'main.py'], 
                           creationflags=subprocess.CREATE_NEW_CONSOLE)
        else:  # Unix/Linux/Mac
            subprocess.Popen([sys.executable, 'main.py'])
        
        # Wait for server to start
        print("⏳ Waiting for MCP server to start...")
        for i in range(10):
            try:
                response = requests.get('http://localhost:8080/health', timeout=2)
                if response.status_code == 200:
                    print("✅ MCP server started successfully!")
                    return True
            except:
                pass
            time.sleep(1)
            print(f"   Attempt {i+1}/10...")
        
        print("❌ MCP server failed to start")
        return False
        
    except Exception as e:
        print(f"❌ Failed to start MCP server: {e}")
        return False

def test_automation():
    """Test the automation with a simple example"""
    print("🧪 Testing automation...")
    
    try:
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
                "text": "Mimicker AI test",
                "description": "Type test query"
            },
            {
                "action": "wait",
                "timeout": 2000,
                "description": "Wait after typing"
            }
        ]
        
        payload = {
            'steps': test_steps,
            'video_id': 'restart_test'
        }
        
        response = requests.post(
            'http://localhost:8080/execute_browser_action',
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print("✅ Automation test successful!")
                return True
            else:
                print(f"❌ Automation test failed: {data.get('error')}")
                return False
        else:
            print(f"❌ Test request failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Test error: {e}")
        return False

def main():
    """Main restart process"""
    print("🔄 RESTARTING MCP SERVER WITH IMPROVED AUTOMATION")
    print("=" * 50)
    
    # Step 1: Stop current server
    stop_mcp_server()
    
    # Step 2: Start new server
    if not start_mcp_server():
        print("\n❌ Failed to restart MCP server")
        print("💡 Try manually:")
        print("   cd MCP_server/MCP_mimic")
        print("   python main.py")
        return False
    
    # Step 3: Test automation
    if test_automation():
        print("\n🎉 SUCCESS! MCP server restarted with improved automation!")
        print("\n🎬 Your video automation should now work better!")
        print("   - Better selector fallbacks")
        print("   - Automatic Enter key press after typing")
        print("   - Improved wait handling")
        print("   - More robust error recovery")
        
        print(f"\n🧪 Test your latest video with:")
        print(f"   python auto_run_latest_video.py")
        return True
    else:
        print("\n⚠️ MCP server started but automation test failed")
        print("💡 Check the server logs for details")
        return False

if __name__ == "__main__":
    try:
        success = main()
        if not success:
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n⏹️ Interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)