#!/usr/bin/env python3
"""
Direct test of browser automation endpoint
"""

import requests
import json

def test_browser_automation_direct():
    """Test browser automation directly"""
    print("🎬 DIRECT BROWSER AUTOMATION TEST")
    print("="*50)
    print("🎯 This will directly test the browser automation endpoint")
    
    # Demo steps that should open visible browser
    demo_steps = [
        {
            "action": "goto",
            "url": "https://example.com",
            "description": "Navigate to example website"
        },
        {
            "action": "wait",
            "timeout": 3000,
            "description": "Wait and show browser for 3 seconds"
        },
        {
            "action": "goto",
            "url": "https://www.google.com",
            "description": "Navigate to Google"
        },
        {
            "action": "wait",
            "timeout": 2000,
            "description": "Wait for Google to load"
        },
        {
            "action": "type",
            "selector": "textarea[name='q']",
            "text": "Mimicker AI Browser Demo",
            "description": "Type in search box"
        },
        {
            "action": "wait",
            "timeout": 3000,
            "description": "Show typed text for 3 seconds"
        }
    ]
    
    print(f"\n📋 Demo Steps:")
    for i, step in enumerate(demo_steps, 1):
        print(f"   {i}. {step['action']}: {step['description']}")
    
    print(f"\n🚀 Executing browser automation...")
    print(f"🎬 A browser window should open and be visible!")
    
    try:
        payload = {
            "steps": demo_steps,
            "video_id": "direct-browser-test"
        }
        
        response = requests.post(
            "http://localhost:8080/execute_browser_action",
            json=payload,
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            
            print(f"\n✅ BROWSER AUTOMATION COMPLETED!")
            print(f"   Success: {result.get('success')}")
            print(f"   Steps Executed: {len(result.get('log', []))}")
            
            if result.get('log'):
                print(f"\n📋 Execution Log:")
                for log_entry in result['log']:
                    print(f"   {log_entry}")
            
            if result.get('success'):
                print(f"\n🎉 SUCCESS!")
                print(f"   ✅ Browser window opened visibly")
                print(f"   ✅ Navigation worked")
                print(f"   ✅ Typing worked")
                print(f"   ✅ All automation steps completed")
                
                print(f"\n🎯 This means your browser automation is working!")
                print(f"   When you click 'Start Analysis', it should trigger this same automation")
                
            else:
                print(f"\n⚠️ Automation completed with issues:")
                print(f"   Error: {result.get('error')}")
                
        else:
            print(f"\n❌ Request failed: {response.status_code}")
            print(f"   Response: {response.text}")
            
    except Exception as e:
        print(f"\n❌ Test error: {e}")
        print(f"\n🔧 Troubleshooting:")
        print(f"   1. Make sure MCP server is running")
        print(f"   2. Check HEADLESS_BROWSER=False in .env")
        print(f"   3. Restart MCP server if needed")
    
    print(f"\n" + "="*60)
    print(f"🎬 DIRECT BROWSER TEST COMPLETE")
    print(f"="*60)

if __name__ == "__main__":
    test_browser_automation_direct()