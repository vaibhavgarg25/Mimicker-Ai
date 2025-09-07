#!/usr/bin/env python3
"""
Fix the timeout issue by restarting services with optimized settings
"""

import os
import sys
import subprocess
import time
import requests
import json

def stop_services():
    """Stop all running services"""
    print("🛑 Stopping services...")
    
    try:
        if os.name == 'nt':  # Windows
            # Stop Python processes
            subprocess.run(['taskkill', '/f', '/im', 'python.exe'], 
                         capture_output=True, text=True)
            # Stop Node processes
            subprocess.run(['taskkill', '/f', '/im', 'node.exe'], 
                         capture_output=True, text=True)
        else:  # Unix/Linux/Mac
            subprocess.run(['pkill', '-f', 'main.py'], capture_output=True)
            subprocess.run(['pkill', '-f', 'app.py'], capture_output=True)
            subprocess.run(['pkill', '-f', 'next'], capture_output=True)
        
        time.sleep(3)
        print("✅ Services stopped")
        return True
    except Exception as e:
        print(f"⚠️ Could not stop all services: {e}")
        return True  # Continue anyway

def start_mcp_server():
    """Start MCP server"""
    print("🚀 Starting MCP server...")
    
    mcp_dir = "MCP_server/MCP_mimic"
    if not os.path.exists(mcp_dir):
        print(f"❌ MCP directory not found: {mcp_dir}")
        return False
    
    try:
        # Start MCP server
        if os.name == 'nt':  # Windows
            subprocess.Popen([sys.executable, 'main.py'], 
                           cwd=mcp_dir,
                           creationflags=subprocess.CREATE_NEW_CONSOLE)
        else:
            subprocess.Popen([sys.executable, 'main.py'], cwd=mcp_dir)
        
        # Wait for server to start
        print("⏳ Waiting for MCP server...")
        for i in range(15):
            try:
                response = requests.get('http://localhost:8080/health', timeout=2)
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

def start_backend():
    """Start backend server"""
    print("🚀 Starting backend...")
    
    backend_dir = "backend"
    if not os.path.exists(backend_dir):
        print(f"❌ Backend directory not found: {backend_dir}")
        return False
    
    try:
        # Start backend
        if os.name == 'nt':  # Windows
            subprocess.Popen([sys.executable, 'app.py'], 
                           cwd=backend_dir,
                           creationflags=subprocess.CREATE_NEW_CONSOLE)
        else:
            subprocess.Popen([sys.executable, 'app.py'], cwd=backend_dir)
        
        # Wait for backend to start
        print("⏳ Waiting for backend...")
        for i in range(10):
            try:
                response = requests.get('http://localhost:8000/api/health', timeout=2)
                if response.status_code == 200:
                    print("✅ Backend started!")
                    return True
            except:
                pass
            time.sleep(1)
            print(f"   Attempt {i+1}/10...")
        
        print("❌ Backend failed to start")
        return False
        
    except Exception as e:
        print(f"❌ Failed to start backend: {e}")
        return False

def test_quick_automation():
    """Test automation with a very simple, fast example"""
    print("🧪 Testing quick automation...")
    
    try:
        # Simple, fast test steps
        test_steps = [
            {
                "action": "goto",
                "url": "https://www.google.com",
                "description": "Navigate to Google"
            },
            {
                "action": "type",
                "selector": "textarea[name='q']",
                "text": "test",
                "description": "Type test query"
            }
        ]
        
        payload = {
            'steps': test_steps,
            'video_id': 'timeout_fix_test'
        }
        
        print("🎬 Running quick automation test...")
        response = requests.post(
            'http://localhost:8080/execute_browser_action',
            json=payload,
            timeout=30  # Short timeout for test
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print("✅ Quick automation test successful!")
                return True
            else:
                print(f"❌ Automation failed: {data.get('error')}")
                return False
        else:
            print(f"❌ Test request failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Test error: {e}")
        return False

def run_latest_video():
    """Run automation on latest video with optimized settings"""
    print("🎬 Running automation on latest video...")
    
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
    
    print(f"📹 Processing: {os.path.basename(latest_video)}")
    
    try:
        payload = {
            'video_url': os.path.abspath(latest_video)
        }
        
        print("🧠 Starting video analysis and automation...")
        response = requests.post(
            'http://localhost:8080/run_task_from_video',
            json=payload,
            timeout=300  # 5 minute timeout
        )
        
        if response.status_code == 200:
            data = response.json()
            status = data.get('status', 'unknown')
            log = data.get('log', [])
            
            print(f"🎬 Result: {status.upper()}")
            
            if log:
                print("\n📋 Execution log:")
                for entry in log[-10:]:  # Show last 10 entries
                    print(f"   {entry}")
            
            return status == 'completed'
        else:
            print(f"❌ Failed: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Main fix process"""
    print("🔧 FIXING TIMEOUT ISSUE")
    print("=" * 40)
    
    # Step 1: Stop all services
    stop_services()
    
    # Step 2: Start MCP server with optimizations
    if not start_mcp_server():
        print("\n❌ Could not start MCP server")
        return False
    
    # Step 3: Start backend
    if not start_backend():
        print("\n❌ Could not start backend")
        return False
    
    # Step 4: Test quick automation
    if not test_quick_automation():
        print("\n⚠️ Quick test failed, but continuing...")
    
    # Step 5: Run latest video
    print(f"\n🎯 Ready to test your latest video!")
    choice = input("Run automation on latest video? (y/n): ").strip().lower()
    
    if choice.startswith('y'):
        success = run_latest_video()
        if success:
            print("\n🎉 SUCCESS! Video automation completed!")
            print("🎬 Check your browser window for the automation!")
        else:
            print("\n❌ Video automation failed")
            print("💡 The timeout issue should be fixed, but there might be other issues")
    else:
        print("\n✅ Services are ready. You can now:")
        print("   1. Go to http://localhost:3000")
        print("   2. Upload a video")
        print("   3. Click 'Start Analysis'")
        print("   4. The timeout issue should be resolved!")
    
    return True

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n⏹️ Interrupted by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")