#!/usr/bin/env python3
"""
Test MCP server browser automation endpoint directly
"""

import requests
import json

def test_mcp_browser_endpoint():
    """Test the MCP server browser automation endpoint"""
    print("🎬 TESTING MCP SERVER BROWSER AUTOMATION ENDPOINT")
    print("="*60)
    print("🎯 This will call the MCP server to open a visible browser")
    
    # Test steps that should open visible browser
    test_steps = [
        {
            "action": "goto",
            "url": "https://example.com",
            "description": "Navigate to example.com - BROWSER SHOULD BE VISIBLE!"
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
    
    print(f"\n📋 Test Steps:")
    for i, step in enumerate(test_steps, 1):
        print(f"   {i}. {step['action']}: {step['description']}")
    
    print(f"\n🚀 Calling MCP server browser automation endpoint...")
    print(f"🎬 BROWSER WINDOW SHOULD OPEN AND BE VISIBLE!")
    
    try:
        payload = {
            "steps": test_steps,
            "video_id": "mcp-browser-test"
        }
        
        response = requests.post(
            "http://localhost:8080/execute_browser_action",
            json=payload,
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            
            print(f"\n✅ MCP SERVER RESPONDED SUCCESSFULLY!")
            print(f"   Success: {result.get('success')}")
            print(f"   Steps Executed: {len(result.get('log', []))}")
            
            if result.get('log'):
                print(f"\n📋 Execution Log:")
                for log_entry in result['log']:
                    print(f"   {log_entry}")
            
            if result.get('success'):
                print(f"\n🎉 SUCCESS!")
                print(f"   ✅ MCP server is working")
                print(f"   ✅ Browser automation executed")
                print(f"   ✅ You should have seen a browser window!")
                
                print(f"\n🎯 This means your 'Start Analysis' should work!")
                print(f"   The same automation happens when you click the button")
                
            else:
                print(f"\n⚠️ Automation completed with issues:")
                print(f"   Error: {result.get('error')}")
                
        else:
            print(f"\n❌ MCP server request failed: {response.status_code}")
            print(f"   Response: {response.text}")
            print(f"\n🔧 Make sure MCP server is running:")
            print(f"   cd MCP_server/MCP_mimic && python main.py")
            
    except Exception as e:
        print(f"\n❌ Test error: {e}")
        print(f"\n🔧 Troubleshooting:")
        print(f"   1. Make sure MCP server is running")
        print(f"   2. Check server shows 'VISIBLE (FORCED FOR DEMO)'")
        print(f"   3. Restart MCP server if needed")
    
    print(f"\n" + "="*60)
    print(f"🎬 MCP BROWSER ENDPOINT TEST COMPLETE")
    print(f"="*60)

if __name__ == "__main__":
    print("🎬 MCP SERVER BROWSER AUTOMATION TEST")
    print("🎯 This tests the exact endpoint your frontend calls")
    print()
    
    input("Press Enter to test MCP server browser automation...")
    test_mcp_browser_endpoint()