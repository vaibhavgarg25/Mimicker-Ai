#!/usr/bin/env python3
"""
Automatically run browser automation on the latest uploaded video.
This script will find the newest video and execute automation without prompts.
"""

import os
import requests
import json
from datetime import datetime

# Configuration
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
    
    print(f"📹 Latest video: {latest_video[2]}")
    return latest_video[0]

def run_automation():
    """Run automation on the latest video"""
    print("🎬 MIMICKER AI - AUTO RUN LATEST VIDEO")
    print("=" * 40)
    
    # Find latest video
    video_path = find_latest_video()
    if not video_path:
        return False
    
    print(f"🎯 Processing: {os.path.basename(video_path)}")
    
    try:
        # Run complete workflow
        payload = {
            'video_url': os.path.abspath(video_path)
        }
        
        print("🧠 Analyzing video and executing automation...")
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
            
            print(f"🎬 Result: {status.upper()}")
            
            if log:
                print("\n📋 What happened:")
                for entry in log[-5:]:  # Show last 5 log entries
                    print(f"   {entry}")
            
            if error:
                print(f"\n❌ Error: {error}")
            
            return status == 'completed'
        else:
            print(f"❌ Failed: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    try:
        success = run_automation()
        if success:
            print("\n🎉 SUCCESS! Check your browser window!")
        else:
            print("\n❌ FAILED! Make sure MCP server is running:")
            print("   cd MCP_server/MCP_mimic && python main.py")
    except KeyboardInterrupt:
        print("\n⏹️ Interrupted by user.")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")