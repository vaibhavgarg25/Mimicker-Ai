#!/usr/bin/env python3
"""
Test browser automation with VERY SLOW and VISIBLE execution
"""
import requests
import json
import os

def test_slow_visible_browser():
    print("🎬 TESTING SLOW VISIBLE BROWSER AUTOMATION")
    print("=" * 60)
    print("🚨 THIS WILL OPEN A BROWSER WINDOW FOR 30+ SECONDS!")
    print("🚨 WATCH YOUR SCREEN CAREFULLY!")
    print("=" * 60)
    
    input("Press Enter to start the SLOW browser test...")
    
    # Create very slow, obvious steps
    slow_steps = [
        {
            "action": "goto",
            "url": "https://www.google.com",
            "description": "Navigate to Google - WATCH THE BROWSER!"
        },
        {
            "action": "wait",
            "timeout": 5000,
            "description": "Wait 5 seconds - BROWSER SHOULD BE VISIBLE!"
        },
        {
            "action": "type",
            "selector": "textarea[name='q']",
            "text": "MIMICKER AI BROWSER TEST - YOU SHOULD SEE THIS TYPING!",
            "description": "Type search query SLOWLY"
        },
        {
            "action": "wait",
            "timeout": 8000,
            "description": "Wait 8 seconds - LOOK AT THE TYPED TEXT!"
        },
        {
            "action": "scroll",
            "direction": "down",
            "amount": 300,
            "description": "Scroll down - WATCH THE PAGE SCROLL!"
        },
        {
            "action": "wait",
            "timeout": 5000,
            "description": "Wait 5 seconds - BROWSER STILL VISIBLE!"
        },
        {
            "action": "goto",
            "url": "https://example.com",
            "description": "Navigate to Example.com - WATCH PAGE CHANGE!"
        },
        {
            "action": "wait",
            "timeout": 10000,
            "description": "Wait 10 seconds - FINAL PAUSE TO SEE BROWSER!"
        }
    ]
    
    print(f"🚀 Starting SLOW browser automation...")
    print(f"🎬 BROWSER WINDOW WILL OPEN AND STAY OPEN FOR 30+ SECONDS!")
    print(f"👀 WATCH YOUR SCREEN NOW!")
    
    try:
        payload = {
            'steps': slow_steps,
            'video_id': 'slow_test_browser'
        }
        
        response = requests.post(
            'http://localhost:8080/execute_browser_action',
            json=payload,
            timeout=120
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"\n✅ BROWSER TEST COMPLETED!")
            print(f"   Success: {result.get('success')}")
            
            if result.get('log'):
                print(f"\n📋 What the browser did:")
                for entry in result['log']:
                    print(f"   {entry}")
            
            print(f"\n🎉 If you saw a browser window, the system is working!")
            print(f"🎉 The 'Start Analysis' button should also open a browser!")
        else:
            print(f"❌ Test failed: {response.status_code}")
            print(f"   Response: {response.text}")
    
    except Exception as e:
        print(f"❌ Test error: {e}")
    
    print(f"\n" + "=" * 60)
    print(f"🎬 SLOW BROWSER TEST COMPLETE")
    print(f"=" * 60)

if __name__ == "__main__":
    test_slow_visible_browser()