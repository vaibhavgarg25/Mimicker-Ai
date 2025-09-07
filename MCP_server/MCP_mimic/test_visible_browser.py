#!/usr/bin/env python3
"""
Direct test to force browser to open visibly
"""

import sys
import os
sys.path.append('.')

from services.browser import BrowserAutomator
import time

def test_visible_browser():
    """Test that browser opens visibly"""
    print("🎬 TESTING VISIBLE BROWSER - THIS SHOULD OPEN A BROWSER WINDOW!")
    print("="*60)
    
    # Create browser automator with forced visible mode
    browser_automator = BrowserAutomator(headless=False)
    
    # Simple test steps
    test_steps = [
        {
            "action": "goto",
            "url": "https://example.com",
            "description": "Navigate to example.com"
        },
        {
            "action": "wait",
            "timeout": 5000,
            "description": "Wait 5 seconds so you can see the browser"
        },
        {
            "action": "goto",
            "url": "https://www.google.com",
            "description": "Navigate to Google"
        },
        {
            "action": "wait",
            "timeout": 3000,
            "description": "Wait 3 seconds at Google"
        }
    ]
    
    print("🚀 EXECUTING BROWSER AUTOMATION...")
    print("🎬 A BROWSER WINDOW SHOULD OPEN NOW!")
    
    try:
        result = browser_automator.execute_steps(test_steps)
        
        print(f"\n✅ BROWSER TEST COMPLETED!")
        print(f"   Success: {result.get('success')}")
        print(f"   Log entries: {len(result.get('log', []))}")
        
        if result.get('log'):
            print(f"\n📋 Execution Log:")
            for log_entry in result['log']:
                print(f"   {log_entry}")
        
        if result.get('success'):
            print(f"\n🎉 SUCCESS! Browser window opened and automation worked!")
        else:
            print(f"\n⚠️ Automation had issues: {result.get('error')}")
            
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("🎬 VISIBLE BROWSER TEST")
    print("🎯 This will FORCE a browser window to open")
    print()
    
    input("Press Enter to start the test (browser will open)...")
    
    success = test_visible_browser()
    
    if success:
        print(f"\n🎉 If you saw a browser window, the system is working!")
        print(f"Now restart your MCP server and try 'Start Analysis' in frontend")
    else:
        print(f"\n❌ Browser test failed - check Playwright installation")