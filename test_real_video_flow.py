#!/usr/bin/env python3
"""
Test the complete video analysis flow with a real video file
"""
import requests
import json
import os

def test_real_video_analysis():
    print("🎬 TESTING REAL VIDEO ANALYSIS FLOW")
    print("=" * 60)
    
    # Check if there are any uploaded videos
    uploads_dir = "backend/uploads"
    if not os.path.exists(uploads_dir):
        print(f"❌ Uploads directory not found: {uploads_dir}")
        print("💡 Upload a video through the frontend first!")
        return
    
    video_files = [f for f in os.listdir(uploads_dir) if f.lower().endswith(('.mp4', '.mov', '.avi', '.mkv', '.webm'))]
    
    if not video_files:
        print(f"❌ No video files found in {uploads_dir}")
        print("💡 Upload a video through the frontend first!")
        return
    
    # Use the first video file found
    video_file = video_files[0]
    video_path = os.path.join(uploads_dir, video_file)
    abs_video_path = os.path.abspath(video_path)
    
    print(f"📹 Found video file: {video_file}")
    print(f"📁 Full path: {abs_video_path}")
    print(f"📊 File size: {os.path.getsize(abs_video_path) / (1024*1024):.2f} MB")
    
    # Test MCP server video analysis
    print("\n🧠 Testing MCP server video analysis...")
    
    payload = {
        'video_url': abs_video_path
    }
    
    try:
        response = requests.post(
            'http://localhost:8080/analyze_video',
            json=payload,
            timeout=60  # Longer timeout for video analysis
        )
        
        print(f"📊 Response Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            steps = result.get('steps', [])
            
            print("✅ VIDEO ANALYSIS SUCCESSFUL!")
            print(f"   Steps extracted: {len(steps)}")
            
            if steps:
                print("\n📋 Extracted Steps:")
                for i, step in enumerate(steps, 1):
                    action = step.get('action', 'unknown')
                    description = step.get('description', 'No description')
                    print(f"   {i}. {action.upper()}: {description}")
                    
                    # Show additional details for specific actions
                    if action == 'goto':
                        print(f"      URL: {step.get('url', 'N/A')}")
                    elif action == 'type':
                        print(f"      Selector: {step.get('selector', 'N/A')}")
                        print(f"      Text: {step.get('text', 'N/A')}")
                    elif action == 'click':
                        print(f"      Selector: {step.get('selector', 'N/A')}")
                
                # Now test browser automation with these real steps
                print(f"\n🤖 Testing browser automation with extracted steps...")
                
                automation_payload = {
                    'steps': steps,
                    'video_id': 'test_real_video'
                }
                
                automation_response = requests.post(
                    'http://localhost:8080/execute_browser_action',
                    json=automation_payload,
                    timeout=120
                )
                
                if automation_response.status_code == 200:
                    auto_result = automation_response.json()
                    print("✅ BROWSER AUTOMATION SUCCESSFUL!")
                    print(f"   Success: {auto_result.get('success')}")
                    
                    if auto_result.get('log'):
                        print("📋 Automation Log:")
                        for entry in auto_result['log']:
                            print(f"   {entry}")
                    
                    if auto_result.get('error'):
                        print(f"❌ Automation Error: {auto_result['error']}")
                else:
                    print(f"❌ Automation failed: {automation_response.status_code}")
                    print(f"   Response: {automation_response.text}")
            else:
                print("⚠️ No steps were extracted from the video")
                print("   This might mean:")
                print("   - Video doesn't show clear browser interactions")
                print("   - Video format not supported")
                print("   - Gemini couldn't analyze the content")
        else:
            print(f"❌ Analysis failed: {response.status_code}")
            print(f"   Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
    
    print("\n" + "=" * 60)
    print("🎬 REAL VIDEO ANALYSIS TEST COMPLETE")
    print("=" * 60)

if __name__ == "__main__":
    test_real_video_analysis()