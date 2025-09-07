#!/usr/bin/env python3
"""
Test backend automation endpoint directly
"""
import requests
import json

def test_backend_automation():
    print("🎬 TESTING BACKEND AUTOMATION ENDPOINT")
    print("=" * 60)
    
    # First, let's check backend health
    try:
        health_response = requests.get('http://localhost:8000/api/health', timeout=5)
        print(f"📊 Backend Health: {health_response.status_code}")
        if health_response.status_code == 200:
            print(f"   {health_response.json()}")
        else:
            print(f"   Error: {health_response.text}")
    except Exception as e:
        print(f"❌ Backend health check failed: {e}")
        return
    
    # Check automation health
    try:
        auto_health = requests.get('http://localhost:8000/api/automation/health', timeout=5)
        print(f"📊 Automation Health: {auto_health.status_code}")
        if auto_health.status_code == 200:
            print(f"   {auto_health.json()}")
        else:
            print(f"   Error: {auto_health.text}")
    except Exception as e:
        print(f"❌ Automation health check failed: {e}")
    
    print("\n🎯 The issue might be:")
    print("   1. You need to be logged in (JWT token required)")
    print("   2. You need to upload a video first")
    print("   3. The video_id needs to exist in the database")
    print("\n💡 To test the full flow:")
    print("   1. Go to http://localhost:3000")
    print("   2. Login/Signup")
    print("   3. Upload ANY video file")
    print("   4. Click 'Start Analysis'")
    print("   5. Browser should open automatically!")

if __name__ == "__main__":
    test_backend_automation()