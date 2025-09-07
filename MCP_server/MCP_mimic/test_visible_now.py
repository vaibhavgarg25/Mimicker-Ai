#!/usr/bin/env python3
"""
Quick test to verify browser opens visibly
"""
from services.browser import BrowserAutomator

def test_visible_browser():
    print("🎬 TESTING VISIBLE BROWSER NOW!")
    print("=" * 50)
    
    # Create browser automator
    automator = BrowserAutomator(headless=True)  # Even with headless=True, it should be visible due to hardcoded False
    
    # Simple test steps
    steps = [
        {
            "action": "goto",
            "url": "https://example.com",
            "description": "Navigate to example.com - BROWSER SHOULD BE VISIBLE!"
        },
        {
            "action": "wait",
            "timeout": 3000,
            "description": "Wait 3 seconds - LOOK FOR THE BROWSER WINDOW!"
        },
        {
            "action": "goto",
            "url": "https://www.google.com",
            "description": "Navigate to Google"
        },
        {
            "action": "type",
            "selector": "textarea[name='q']",
            "text": "VISIBLE BROWSER TEST - YOU SHOULD SEE THIS!",
            "description": "Type in Google search box"
        },
        {
            "action": "wait",
            "timeout": 5000,
            "description": "Wait 5 seconds to see the typed text"
        }
    ]
    
    print("🚀 Executing browser automation...")
    print("🎬 BROWSER WINDOW SHOULD OPEN AND BE VISIBLE!")
    
    result = automator.execute_steps(steps)
    
    print("\n✅ RESULT:")
    print(f"   Success: {result['success']}")
    if result.get('log'):
        print("📋 Execution Log:")
        for entry in result['log']:
            print(f"   {entry}")
    
    if result.get('error'):
        print(f"❌ Error: {result['error']}")
    else:
        print("🎉 SUCCESS! Browser window should have opened and been visible!")
        print("🎉 If you saw a browser window, the automation is working correctly!")

if __name__ == "__main__":
    test_visible_browser()