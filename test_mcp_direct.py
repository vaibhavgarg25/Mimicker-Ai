#!/usr/bin/env python3
"""
Test MCP server browser automation directly
"""
import requests
import json

def test_mcp_browser_automation():
    print("🎬 TESTING MCP SERVER BROWSER AUTOMATION")
    print("=" * 60)
    
    # Test steps that should show visible browser
    demo_steps = [
        {
            "action": "goto",
            "url": "https://example.com",
            "description": "Navigate to example website - BROWSER SHOULD BE VISIBLE!"
        },
        {
            "action": "wait",
            "timeout": 5000,
            "description": "Wait 5 seconds - LOOK FOR THE BROWSER WINDOW!"
        },
        {
            "action": "goto",
            "url": "https://www.google.com",
            "description": "Navigate to Google"
        },
        {
            "action": "type",
            "selector": "textarea[name='q']",
            "text": "MIMICKER AI BROWSER TEST - YOU SHOULD SEE THIS!",
            "description": "Type in Google search box"
        },
        {
            "action": "wait",
            "timeout": 5000,
            "description": "Wait 5 seconds to see the typed text"
        }
    ]
    
    payload = {
        'steps': demo_steps,
        'video_id': 'test_video_123'
    }
    
    print("🚀 Calling MCP server browser automation endpoint...")
    print("🎬 BROWSER WINDOW SHOULD OPEN AND BE VISIBLE!")
    
    try:
        response = requests.post(
            'http://localhost:8080/execute_browser_action',
            json=payload,
            timeout=60
        )
        
        print(f"\n📊 Response Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ MCP SERVER RESPONDED SUCCESSFULLY!")
            print(f"   Success: {result.get('success')}")
            print(f"   Steps Executed: {len(result.get('log', []))}")
            
            if result.get('log'):
                print("📋 Execution Log:")
                for entry in result['log']:
                    print(f"   {entry}")
            
            if result.get('error'):
                print(f"❌ Error: {result['error']}")
            else:
                print("🎉 SUCCESS!")
                print("   ✅ MCP server is working")
                print("   ✅ Browser automation executed")
                print("   ✅ You should have seen a browser window!")
        else:
            print(f"❌ MCP server error: {response.status_code}")
            print(f"   Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Failed to connect to MCP server: {e}")
    
    print("\n" + "=" * 60)
    print("🎬 MCP BROWSER ENDPOINT TEST COMPLETE")
    print("=" * 60)

if __name__ == "__main__":
    test_mcp_browser_automation()