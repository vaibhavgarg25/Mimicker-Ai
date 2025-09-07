#!/usr/bin/env python3
"""
Test authentication flow
"""

import requests
import json

BACKEND_URL = "http://localhost:8000"

def test_signup_and_auth():
    """Test signup and authentication flow"""
    print("🧪 Testing Authentication Flow")
    
    # Test signup
    print("\n📝 Testing Signup...")
    signup_data = {
        "name": "Test User",
        "email": "test@example.com",
        "password": "testpass123"
    }
    
    try:
        response = requests.post(f"{BACKEND_URL}/api/auth/signup", json=signup_data)
        print(f"Signup Status: {response.status_code}")
        
        if response.status_code == 201:
            data = response.json()
            print("✅ Signup successful!")
            print(f"   Token received: {data['data']['token'][:20]}...")
            token = data['data']['token']
            
            # Test authenticated request
            print("\n🔐 Testing Authenticated Request...")
            headers = {"Authorization": f"Bearer {token}"}
            
            videos_response = requests.get(f"{BACKEND_URL}/api/videos/my-videos", headers=headers)
            print(f"Videos Request Status: {videos_response.status_code}")
            
            if videos_response.status_code == 200:
                print("✅ Authentication working!")
                videos_data = videos_response.json()
                print(f"   Videos: {videos_data}")
            else:
                print(f"❌ Authentication failed: {videos_response.text}")
                
        elif response.status_code == 409:
            print("⚠️ User already exists, testing login...")
            
            # Test login
            login_data = {
                "email": "test@example.com",
                "password": "testpass123"
            }
            
            login_response = requests.post(f"{BACKEND_URL}/api/auth/login", json=login_data)
            print(f"Login Status: {login_response.status_code}")
            
            if login_response.status_code == 200:
                data = login_response.json()
                print("✅ Login successful!")
                token = data['data']['token']
                
                # Test authenticated request
                print("\n🔐 Testing Authenticated Request...")
                headers = {"Authorization": f"Bearer {token}"}
                
                videos_response = requests.get(f"{BACKEND_URL}/api/videos/my-videos", headers=headers)
                print(f"Videos Request Status: {videos_response.status_code}")
                
                if videos_response.status_code == 200:
                    print("✅ Authentication working!")
                else:
                    print(f"❌ Authentication failed: {videos_response.text}")
            else:
                print(f"❌ Login failed: {login_response.text}")
        else:
            print(f"❌ Signup failed: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_signup_and_auth()