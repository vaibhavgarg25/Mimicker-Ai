#!/usr/bin/env python3
"""
Integration test script for Mimicker AI
Tests the complete workflow: Backend -> MCP Server -> Analysis -> Automation
"""

import requests
import time
import json
import os

# Configuration
BACKEND_URL = "http://localhost:8000"
MCP_URL = "http://localhost:3000"

def test_health_checks():
    """Test if all services are running"""
    print("🔍 Testing service health...")
    
    # Test Backend
    try:
        response = requests.get(f"{BACKEND_URL}/api/health", timeout=5)
        if response.status_code == 200:
            print("✅ Backend is healthy")
        else:
            print(f"❌ Backend health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Backend is not accessible: {e}")
        return False
    
    # Test MCP Server
    try:
        response = requests.get(f"{MCP_URL}/health", timeout=5)
        if response.status_code == 200:
            print("✅ MCP Server is healthy")
        else:
            print(f"❌ MCP Server health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ MCP Server is not accessible: {e}")
        return False
    
    return True

def test_mcp_analysis():
    """Test MCP server video analysis"""
    print("\n🎬 Testing MCP video analysis...")
    
    # Test with a sample video URL (fallback to example steps)
    test_payload = {
        "video_url": "https://example.com/test-video.mp4"
    }
    
    try:
        response = requests.post(f"{MCP_URL}/analyze_video", json=test_payload, timeout=30)
        if response.status_code == 200:
            data = response.json()
            steps = data.get('steps', [])
            print(f"✅ Video analysis successful - {len(steps)} steps extracted")
            print(f"   Sample step: {steps[0] if steps else 'No steps'}")
            return True
        else:
            print(f"❌ Video analysis failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ Video analysis error: {e}")
        return False

def test_automation_health():
    """Test automation service health"""
    print("\n🤖 Testing automation service...")
    
    try:
        response = requests.get(f"{BACKEND_URL}/api/automation/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("✅ Automation service is healthy")
            print(f"   MCP Server status: {data['data']['mcp_server']}")
            return True
        else:
            print(f"❌ Automation health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Automation service error: {e}")
        return False

def main():
    """Run all integration tests"""
    print("🚀 Starting Mimicker AI Integration Tests\n")
    
    tests = [
        ("Service Health Checks", test_health_checks),
        ("MCP Video Analysis", test_mcp_analysis),
        ("Automation Service", test_automation_health),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "="*50)
    print("📊 TEST RESULTS SUMMARY")
    print("="*50)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
        if result:
            passed += 1
    
    print(f"\nTotal: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("\n🎉 All tests passed! Your Mimicker AI integration is working correctly.")
        print("\nNext steps:")
        print("1. Open http://localhost:3000 in your browser")
        print("2. Sign up for an account")
        print("3. Upload a video to test the full workflow")
    else:
        print("\n⚠️  Some tests failed. Please check the services and try again.")
        print("\nTroubleshooting:")
        print("1. Make sure all services are running (use start_all.bat)")
        print("2. Check your .env files have the correct configuration")
        print("3. Verify MongoDB is running")
        print("4. Ensure you have a valid Gemini API key")

if __name__ == "__main__":
    main()