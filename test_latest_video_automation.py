#!/usr/bin/env python3
"""
Test script to automatically process the latest uploaded video
and execute browser automation based on its content.
"""

import os
import sys
import requests
import json
import time
from datetime import datetime

# Configuration
BACKEND_URL = "http://localhost:8000"
MCP_SERVER_URL = "http://localhost:8080"
UPLOADS_DIR = "backend/uploads"

def find_latest_video():
    """Find the most recently uploaded video file"""
    if not os.path.exists(UPLOADS_DIR):
        print(f"❌ Uploads directory not found: {UPLOADS_DIR}")
        return None
    
    video_files = []
    for filename in os.listdir(UPLOADS_DIR):
        if filename.lower().endswith(('.mp4', '.mov', '.avi', '.mkv', '.webm')):
            filepath = os.path.join(UPLOADS_DIR, filename)
            mtime = os.path.getmtime(filepath)
            video_files.append((filepath, mtime, filename))
    
    if not video_files:
        print("❌ No video files found in uploads directory")
        return None
    
    # Sort by modification time (newest first)
    video_files.sort(key=lambda x: x[1], reverse=True)
    latest_video = video_files[0]
    
    print(f"📹 Found latest video: {latest_video[2]}")
    print(f"📅 Upload time: {datetime.fromtimestamp(latest_video[1])}")
    return latest_video[0]

def check_services():
    """Check if backend and MCP server are running"""
    print("🔍 Checking services...")
    
    # Check backend
    try:
        response = requests.get(f"{BACKEND_URL}/api/health", timeout=5)
        if response.status_code == 200:
            print("✅ Backend is running")
        else:
            print(f"⚠️ Backend returned status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Backend is not running: {e}")
        return False
    
    # Check MCP server
    try:
        response = requests.get(f"{MCP_SERVER_URL}/health", timeout=5)
        if response.status_code == 200:
            print("✅ MCP server is running")
        else:
            print(f"⚠️ MCP server returned status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ MCP server is not running: {e}")
        print("💡 Start it with: cd MCP_server/MCP_mimic && python main.py")
        return False
    
    return True

def analyze_video_direct(video_path):
    """Analyze video directly through MCP server"""
    print(f"🧠 Analyzing video: {video_path}")
    
    try:
        payload = {
            'video_url': os.path.abspath(video_path)
        }
        
        response = requests.post(
            f"{MCP_SERVER_URL}/analyze_video",
            json=payload,
            timeout=60
        )
        
        if response.status_code == 200:
            data = response.json()
            steps = data.get('steps', [])
            print(f"✅ Analysis completed! Extracted {len(steps)} steps:")
            
            for i, step in enumerate(steps, 1):
                action = step.get('action', 'unknown')
                desc = step.get('description', 'No description')
                print(f"   {i}. {action}: {desc}")
            
            return steps
        else:
            print(f"❌ Analysis failed: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Analysis error: {e}")
        return None

def execute_automation_direct(steps):
    """Execute automation directly through MCP server"""
    print(f"🤖 Executing {len(steps)} automation steps...")
    
    try:
        payload = {
            'steps': steps,
            'video_id': 'test_latest_video'
        }
        
        response = requests.post(
            f"{MCP_SERVER_URL}/execute_browser_action",
            json=payload,
            timeout=120
        )
        
        if response.status_code == 200:
            data = response.json()
            success = data.get('success', False)
            log = data.get('log', [])
            error = data.get('error')
            
            print(f"🎬 Automation {'completed' if success else 'failed'}!")
            
            if log:
                print("📋 Execution log:")
                for entry in log:
                    print(f"   {entry}")
            
            if error:
                print(f"❌ Error: {error}")
            
            return success
        else:
            print(f"❌ Automation failed: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Automation error: {e}")
        return False

def run_complete_workflow(video_path):
    """Run the complete workflow through MCP server"""
    print(f"🚀 Running complete workflow for: {video_path}")
    
    try:
        payload = {
            'video_url': os.path.abspath(video_path)
        }
        
        response = requests.post(
            f"{MCP_SERVER_URL}/run_task_from_video",
            json=payload,
            timeout=180
        )
        
        if response.status_code == 200:
            data = response.json()
            status = data.get('status', 'unknown')
            log = data.get('log', [])
            error = data.get('error')
            
            print(f"🎬 Workflow {status}!")
            
            if log:
                print("📋 Execution log:")
                for entry in log:
                    print(f"   {entry}")
            
            if error:
                print(f"❌ Error: {error}")
            
            return status == 'completed'
        else:
            print(f"❌ Workflow failed: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Workflow error: {e}")
        return False

def main():
    """Main execution function"""
    print("🎬 MIMICKER AI - LATEST VIDEO AUTOMATION TEST")
    print("=" * 50)
    
    # Step 1: Check services
    if not check_services():
        print("\n❌ Services not ready. Please start them first:")
        print("   Backend: cd backend && python app.py")
        print("   MCP Server: cd MCP_server/MCP_mimic && python main.py")
        return False
    
    # Step 2: Find latest video
    video_path = find_latest_video()
    if not video_path:
        print("\n❌ No video found. Please upload a video first.")
        return False
    
    print(f"\n🎯 Processing video: {os.path.basename(video_path)}")
    
    # Step 3: Choose execution method
    print("\n🔧 Choose execution method:")
    print("1. Complete workflow (analyze + execute)")
    print("2. Step by step (analyze first, then execute)")
    
    choice = input("Enter choice (1 or 2): ").strip()
    
    if choice == "1":
        # Complete workflow
        success = run_complete_workflow(video_path)
        if success:
            print("\n🎉 SUCCESS! Video automation completed!")
        else:
            print("\n❌ FAILED! Check the logs above for details.")
    
    elif choice == "2":
        # Step by step
        steps = analyze_video_direct(video_path)
        if not steps:
            print("\n❌ Analysis failed. Cannot proceed.")
            return False
        
        print(f"\n🤖 Ready to execute {len(steps)} steps. Continue? (y/n): ", end="")
        if input().lower().startswith('y'):
            success = execute_automation_direct(steps)
            if success:
                print("\n🎉 SUCCESS! Video automation completed!")
            else:
                print("\n❌ FAILED! Check the logs above for details.")
        else:
            print("\n⏹️ Execution cancelled by user.")
    
    else:
        print("\n❌ Invalid choice. Exiting.")
        return False
    
    return True

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹️ Interrupted by user. Exiting...")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)