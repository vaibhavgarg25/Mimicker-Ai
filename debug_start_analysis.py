#!/usr/bin/env python3
"""
Debug the "Start Analysis" button flow
"""
import requests
import json
import os
import time

def debug_start_analysis_flow():
    print("🔍 DEBUGGING 'START ANALYSIS' BUTTON FLOW")
    print("=" * 60)
    
    # Step 1: Check all services are running
    print("📊 Step 1: Checking service health...")
    
    services = {
        "Frontend": "http://localhost:3000",
        "Backend": "http://localhost:8000/api/health", 
        "MCP Server": "http://localhost:8080/health",
        "Automation": "http://localhost:8000/api/automation/health"
    }
    
    for service, url in services.items():
        try:
            if service == "Frontend":
                # Just check if port is open
                import socket
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                result = sock.connect_ex(('localhost', 3000))
                sock.close()
                status = "✅ Running" if result == 0 else "❌ Not running"
            else:
                response = requests.get(url, timeout=5)
                status = "✅ Running" if response.status_code == 200 else f"❌ Error {response.status_code}"
        except Exception as e:
            status = f"❌ Failed: {str(e)}"
        
        print(f"   {service}: {status}")
    
    # Step 2: Check if we have uploaded videos
    print(f"\n📹 Step 2: Checking uploaded videos...")
    uploads_dir = "backend/uploads"
    
    if not os.path.exists(uploads_dir):
        print(f"❌ No uploads directory found: {uploads_dir}")
        print("💡 You need to upload a video through the frontend first!")
        return
    
    video_files = [f for f in os.listdir(uploads_dir) if f.lower().endswith(('.mp4', '.mov', '.avi', '.mkv', '.webm'))]
    
    if not video_files:
        print(f"❌ No video files found in {uploads_dir}")
        print("💡 Upload a video through the frontend first!")
        return
    
    print(f"✅ Found {len(video_files)} video file(s):")
    for video in video_files:
        size_mb = os.path.getsize(os.path.join(uploads_dir, video)) / (1024*1024)
        print(f"   - {video} ({size_mb:.2f} MB)")
    
    # Step 3: Test the complete flow manually
    video_file = video_files[0]
    video_path = os.path.join(uploads_dir, video_file)
    abs_video_path = os.path.abspath(video_path)
    
    print(f"\n🧪 Step 3: Testing complete flow with {video_file}...")
    
    # Test 3a: Video Analysis
    print("   3a. Testing video analysis...")
    try:
        analysis_payload = {'video_url': abs_video_path}
        analysis_response = requests.post(
            'http://localhost:8080/analyze_video',
            json=analysis_payload,
            timeout=60
        )
        
        if analysis_response.status_code == 200:
            analysis_result = analysis_response.json()
            steps = analysis_result.get('steps', [])
            print(f"   ✅ Analysis successful: {len(steps)} steps extracted")
            
            # Show first few steps
            for i, step in enumerate(steps[:3], 1):
                action = step.get('action', 'unknown')
                desc = step.get('description', 'No description')[:50]
                print(f"      {i}. {action.upper()}: {desc}...")
        else:
            print(f"   ❌ Analysis failed: {analysis_response.status_code}")
            print(f"      Response: {analysis_response.text[:200]}...")
            return
    except Exception as e:
        print(f"   ❌ Analysis error: {e}")
        return
    
    # Test 3b: Browser Automation
    print("   3b. Testing browser automation...")
    print("   🎬 BROWSER WINDOW SHOULD OPEN NOW!")
    
    try:
        automation_payload = {
            'steps': steps,
            'video_id': f'debug_test_{int(time.time())}'
        }
        
        automation_response = requests.post(
            'http://localhost:8080/execute_browser_action',
            json=automation_payload,
            timeout=120
        )
        
        if automation_response.status_code == 200:
            auto_result = automation_response.json()
            print(f"   ✅ Automation completed: Success = {auto_result.get('success')}")
            
            if auto_result.get('log'):
                print("   📋 Automation log (last 3 entries):")
                for entry in auto_result['log'][-3:]:
                    print(f"      {entry}")
            
            if auto_result.get('error'):
                print(f"   ⚠️ Automation had issues: {auto_result['error']}")
        else:
            print(f"   ❌ Automation failed: {automation_response.status_code}")
            print(f"      Response: {automation_response.text[:200]}...")
    except Exception as e:
        print(f"   ❌ Automation error: {e}")
    
    # Step 4: Check what might be wrong with frontend flow
    print(f"\n🔍 Step 4: Diagnosing frontend flow issues...")
    
    print("   Common issues when 'Start Analysis' doesn't work:")
    print("   1. ❓ Not logged in (need JWT token)")
    print("   2. ❓ Video not properly uploaded to database")
    print("   3. ❓ Frontend not calling correct API endpoint")
    print("   4. ❓ Backend not starting async processing")
    print("   5. ❓ MCP server not receiving requests")
    
    print(f"\n💡 To fix 'Start Analysis' button:")
    print("   1. Make sure you're logged in to the frontend")
    print("   2. Upload a video and wait for upload to complete")
    print("   3. Check browser developer console for errors")
    print("   4. Check backend terminal for processing logs")
    print("   5. Check MCP server terminal for automation logs")
    
    print(f"\n🎬 Expected flow when 'Start Analysis' works:")
    print("   1. Frontend → POST /api/automation/trigger/{video_id}")
    print("   2. Backend → Starts async thread")
    print("   3. Backend → Calls MCP server for analysis")
    print("   4. MCP server → Analyzes video with Gemini")
    print("   5. MCP server → Executes browser automation")
    print("   6. Browser → Opens and performs video actions")
    
    print(f"\n" + "=" * 60)
    print("🔍 DEBUG COMPLETE")
    print("=" * 60)

if __name__ == "__main__":
    debug_start_analysis_flow()