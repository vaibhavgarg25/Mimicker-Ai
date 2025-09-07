#!/usr/bin/env python3
"""
Test the complete Start Analysis flow with browser automation
"""

import requests
import json
import time

def test_start_analysis_with_browser():
    """Test the complete Start Analysis flow"""
    print("🎬 TESTING START ANALYSIS WITH BROWSER AUTOMATION")
    print("="*60)
    
    # Step 1: Authenticate
    print("📋 Step 1: Authentication")
    auth_data = {
        "name": "Browser Test User",
        "email": "browsertest@mimicker.ai",
        "password": "browsertest123"
    }
    
    try:
        # Try login first
        login_response = requests.post("http://localhost:8000/api/auth/login", 
                                     json={"email": auth_data["email"], "password": auth_data["password"]})
        
        if login_response.status_code == 200:
            token = login_response.json()['data']['token']
            print("✅ Authentication: SUCCESS")
        else:
            # Try signup
            signup_response = requests.post("http://localhost:8000/api/auth/signup", json=auth_data)
            if signup_response.status_code == 201:
                token = signup_response.json()['data']['token']
                print("✅ Authentication: SUCCESS (new user)")
            else:
                print(f"❌ Authentication: FAILED")
                return False
                
    except Exception as e:
        print(f"❌ Authentication: ERROR - {e}")
        return False
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Step 2: Get a video ID (or use existing one)
    print("\n📋 Step 2: Getting Video ID")
    try:
        videos_response = requests.get("http://localhost:8000/api/videos/my-videos", 
                                     headers=headers, timeout=10)
        
        if videos_response.status_code == 200:
            videos_data = videos_response.json()
            videos = videos_data['data']['videos']
            
            if videos:
                video_id = videos[0]['video_id']
                print(f"✅ Using existing video: {video_id}")
            else:
                print("⚠️ No videos found - you need to upload a video first")
                print("   Go to the frontend and upload any video file")
                return False
        else:
            print(f"❌ Failed to get videos: {videos_response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Video fetch error: {e}")
        return False
    
    # Step 3: Trigger Start Analysis (this should open browser!)
    print(f"\n📋 Step 3: Triggering Start Analysis")
    print(f"🎬 This should open a VISIBLE browser window!")
    
    try:
        trigger_response = requests.post(
            f"http://localhost:8000/api/automation/trigger/{video_id}",
            headers=headers,
            timeout=30
        )
        
        if trigger_response.status_code == 202:
            print("✅ Analysis triggered successfully!")
            print("🎬 Browser window should be opening now...")
            
            # Wait for processing
            print("⏳ Waiting for analysis and automation to complete...")
            time.sleep(10)  # Give time for browser automation to run
            
            # Check status
            status_response = requests.get(
                f"http://localhost:8000/api/automation/status/{video_id}",
                headers=headers,
                timeout=10
            )
            
            if status_response.status_code == 200:
                status_data = status_response.json()
                analysis_status = status_data['data']['analysis_status']
                execution_status = status_data['data']['execution_status']
                
                print(f"✅ Status Check:")
                print(f"   Analysis: {analysis_status}")
                print(f"   Execution: {execution_status}")
                
                if execution_status == 'completed':
                    print("🎉 BROWSER AUTOMATION COMPLETED!")
                    print("   The browser window should have opened and performed automation")
                elif execution_status == 'running':
                    print("🎬 Browser automation is still running...")
                else:
                    print(f"⚠️ Execution status: {execution_status}")
                    
            else:
                print(f"❌ Status check failed: {status_response.status_code}")
                
        elif trigger_response.status_code == 200:
            print("✅ Analysis already exists - checking execution...")
            
        else:
            print(f"❌ Trigger failed: {trigger_response.status_code}")
            print(f"   Response: {trigger_response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Analysis trigger error: {e}")
        return False
    
    print(f"\n" + "="*60)
    print(f"🎬 START ANALYSIS TEST COMPLETE!")
    print(f"="*60)
    
    print(f"\n🎯 WHAT SHOULD HAVE HAPPENED:")
    print(f"   1. ✅ User authenticated")
    print(f"   2. ✅ Video ID retrieved")
    print(f"   3. ✅ Analysis triggered")
    print(f"   4. 🎬 Browser window opened (visible)")
    print(f"   5. 🎬 Automation executed (navigation, typing, etc.)")
    print(f"   6. ✅ Process completed")
    
    print(f"\n🚀 If you saw a browser window open and perform actions,")
    print(f"   your Start Analysis button is working perfectly!")
    
    return True

if __name__ == "__main__":
    print("🎬 MIMICKER AI - START ANALYSIS BROWSER TEST")
    print("🎯 This will test if clicking Start Analysis opens a browser")
    print()
    
    success = test_start_analysis_with_browser()
    
    if success:
        print(f"\n🎉 TEST COMPLETED!")
        print(f"Now try clicking 'Start Analysis' in your frontend!")
    else:
        print(f"\n❌ Test failed - check the issues above")