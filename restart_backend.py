#!/usr/bin/env python3
"""
Automated backend restart script
"""

import subprocess
import time
import requests
import os
import signal
import psutil

def find_backend_process():
    """Find running backend process"""
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            cmdline = proc.info['cmdline']
            if cmdline and len(cmdline) > 1:
                if 'python' in cmdline[0] and 'app.py' in cmdline[1]:
                    return proc.info['pid']
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return None

def stop_backend():
    """Stop the running backend process"""
    pid = find_backend_process()
    if pid:
        try:
            print(f"🛑 Stopping backend process (PID: {pid})")
            os.kill(pid, signal.SIGTERM)
            time.sleep(2)
            return True
        except:
            print("⚠️ Could not stop backend process automatically")
            return False
    else:
        print("ℹ️ No backend process found running")
        return True

def start_backend():
    """Start the backend process"""
    try:
        print("🚀 Starting backend...")
        os.chdir('backend')
        
        # Start backend in background
        process = subprocess.Popen(
            ['python', 'app.py'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Wait a moment for startup
        time.sleep(3)
        
        # Check if it's running
        if process.poll() is None:
            print("✅ Backend started successfully")
            return True
        else:
            stdout, stderr = process.communicate()
            print(f"❌ Backend failed to start:")
            print(f"   stdout: {stdout.decode()}")
            print(f"   stderr: {stderr.decode()}")
            return False
            
    except Exception as e:
        print(f"❌ Error starting backend: {e}")
        return False

def test_backend():
    """Test if backend is working with correct MCP configuration"""
    try:
        print("🧪 Testing backend connection...")
        
        # Test health endpoint
        response = requests.get("http://localhost:8000/api/automation/health", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            mcp_status = data['data']['mcp_server']
            
            print(f"✅ Backend is running")
            print(f"   MCP Server Status: {mcp_status}")
            
            if mcp_status == 'healthy':
                print("🎉 Backend is now properly connected to MCP server!")
                return True
            else:
                print("⚠️ Backend still can't connect to MCP server")
                return False
        else:
            print(f"❌ Backend health check failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Backend test failed: {e}")
        return False

def main():
    """Main restart process"""
    print("🔄 Automated Backend Restart Process")
    print("="*50)
    
    # Step 1: Stop current backend
    if not stop_backend():
        print("\n⚠️ Please manually stop your backend process:")
        print("   1. Go to your backend terminal")
        print("   2. Press Ctrl+C to stop the process")
        print("   3. Run this script again")
        return False
    
    # Step 2: Start new backend
    if not start_backend():
        print("\n❌ Automated start failed. Please start manually:")
        print("   cd backend")
        print("   python app.py")
        return False
    
    # Step 3: Test the backend
    if test_backend():
        print("\n🎉 SUCCESS! Backend restarted with correct MCP configuration")
        print("\n📱 Your 'Start Analysis' button should now work!")
        print("\n🧪 Test it by:")
        print("   1. Go to http://localhost:3000")
        print("   2. Upload a video")
        print("   3. Click 'Start Analysis'")
        return True
    else:
        print("\n❌ Backend restarted but MCP connection still not working")
        print("\n🔧 Manual troubleshooting needed:")
        print("   1. Check MCP server is running: cd MCP_server/MCP_mimic && python main.py")
        print("   2. Check .env file has: MCP_SERVER_URL=http://localhost:8080")
        return False

if __name__ == "__main__":
    main()