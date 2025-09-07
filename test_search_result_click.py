#!/usr/bin/env python3
"""
Test script specifically for testing Google search and clicking on results
"""

import requests
import json
import time

MCP_SERVER_URL = "http://localhost:8080"

def test_search_and_click():
    """Test searching and clicking on first result"""
    print("🧪 Testing Google search and result clicking...")
    
    # Test steps that simulate searching and clicking first result
    test_steps = [
        {
            "action": "goto",
            "url": "https://www.google.com",
            "description": "Navigate to Google search"
        },
        {
            "action": "wait",
            "timeout": 2000,
            "description": "Wait for page to load"
        },
        {
            "action": "type",
            "selector": "textarea[name='q']",
            "text": "YouTube",
            "description": "Type YouTube search query"
        },
        {
            "action": "wait",
            "timeout": 1000,
            "description": "Wait after typing"
        },
        {
            "action": "click",
            "selector": "input[name='btnK']",
            "description": "Click Google Search button"
        },
        {
            "action": "wait",
            "timeout": 4000,
            "description": "Wait for search results to load"
        },
        {
            "action": "click",
            "selector": "h3 a",
            "description": "Click on first search result"
        },
        {
            "action": "wait",
            "timeout": 5000,
            "description": "Wait for result page to load"
        }
    ]
    
    try:
        payload = {
            'steps': test_steps,
            'video_id': 'search_result_test'
        }
        
        print("🎬 Running search result click test...")
        response = requests.post(
            f"{MCP_SERVER_URL}/execute_browser_action",
            json=payload,
            timeout=60
        )
        
        if response.status_code == 200:
            data = response.json()
            success = data.get('success', False)
            log = data.get('log', [])
            error = data.get('error')
            
            print(f"🎬 Test {'PASSED' if success else 'FAILED'}!")
            
            if log:
                print("\n📋 Execution log:")
                for entry in log:
                    print(f"   {entry}")
            
            if error:
                print(f"\n❌ Error: {error}")
            
            return success
        else:
            print(f"❌ Test request failed: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Test error: {e}")
        return False

def check_mcp_server():
    """Check if MCP server is running"""
    try:
        response = requests.get(f"{MCP_SERVER_URL}/health", timeout=5)
        return response.status_code == 200
    except:
        return False

def main():
    """Main test function"""
    print("🔍 GOOGLE SEARCH RESULT CLICK TEST")
    print("=" * 40)
    
    # Check MCP server
    if not check_mcp_server():
        print("❌ MCP server is not running!")
        print("💡 Start it with: cd MCP_server/MCP_mimic && python main.py")
        return False
    
    print("✅ MCP server is running")
    
    # Run test
    success = test_search_and_click()
    
    if success:
        print("\n🎉 SUCCESS! Search result clicking is working!")
        print("🎬 The browser should have:")
        print("   1. Opened Google")
        print("   2. Searched for 'YouTube'")
        print("   3. Clicked on the first result")
        print("   4. Navigated to the result page")
    else:
        print("\n❌ FAILED! Search result clicking needs more work")
        print("💡 Check the execution log above for details")
    
    return success

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n⏹️ Test interrupted by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")