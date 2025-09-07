#!/usr/bin/env python3
"""
Demo browser automation for project review
This will show live browser automation to the reviewer!
"""

import requests
import json
import time

def demo_browser_automation():
    """Demo browser automation with visible browser for reviewer"""
    print("🎬 BROWSER AUTOMATION DEMO FOR PROJECT REVIEW")
    print("="*60)
    print("🎯 This will open a VISIBLE browser window for demonstration!")
    print("="*60)
    
    # Demo automation steps - designed to be impressive for reviewers
    demo_steps = [
        {
            "action": "goto",
            "url": "https://example.com",
            "description": "Navigate to example website"
        },
        {
            "action": "wait",
            "timeout": 2000,
            "description": "Wait for page to load"
        },
        {
            "action": "scroll",
            "direction": "down",
            "amount": 300,
            "description": "Scroll down to see more content"
        },
        {
            "action": "wait",
            "timeout": 1500,
            "description": "Pause for demonstration"
        },
        {
            "action": "goto",
            "url": "https://httpbin.org/forms/post",
            "description": "Navigate to a form for interaction demo"
        },
        {
            "action": "wait",
            "timeout": 2000,
            "description": "Wait for form to load"
        },
        {
            "action": "type",
            "selector": "input[name='custname']",
            "text": "Mimicker AI Demo",
            "description": "Fill in customer name field"
        },
        {
            "action": "wait",
            "timeout": 1000,
            "description": "Pause to show typing"
        },
        {
            "action": "type",
            "selector": "input[name='custtel']",
            "text": "555-DEMO-AI",
            "description": "Fill in telephone field"
        },
        {
            "action": "wait",
            "timeout": 1000,
            "description": "Pause to show typing"
        },
        {
            "action": "type",
            "selector": "input[name='custemail']",
            "text": "demo@mimicker.ai",
            "description": "Fill in email field"
        },
        {
            "action": "wait",
            "timeout": 1000,
            "description": "Pause to show typing"
        },
        {
            "action": "select",
            "selector": "select[name='size']",
            "value": "large",
            "description": "Select pizza size"
        },
        {
            "action": "wait",
            "timeout": 1000,
            "description": "Pause to show selection"
        },
        {
            "action": "scroll",
            "direction": "down",
            "amount": 200,
            "description": "Scroll to see submit button"
        },
        {
            "action": "wait",
            "timeout": 2000,
            "description": "Final pause before completion"
        }
    ]
    
    print(f"\n📋 Demo Steps Prepared:")
    for i, step in enumerate(demo_steps, 1):
        print(f"   {i}. {step['action']}: {step['description']}")
    
    print(f"\n🚀 Starting Browser Automation Demo...")
    print(f"⚠️  A browser window will open - this is for the demo!")
    
    try:
        # Send automation request to MCP server
        automation_payload = {
            "steps": demo_steps,
            "video_id": "project-review-demo"
        }
        
        print(f"\n📡 Sending automation request to MCP server...")
        
        automation_response = requests.post(
            "http://localhost:8080/execute_browser_action", 
            json=automation_payload, 
            timeout=120  # Extended timeout for demo
        )
        
        if automation_response.status_code == 200:
            result = automation_response.json()
            
            print(f"\n✅ BROWSER AUTOMATION DEMO COMPLETED!")
            print(f"   🎯 Success: {result.get('success')}")
            print(f"   📊 Steps Executed: {len(result.get('log', []))}")
            
            # Show execution log
            if result.get('log'):
                print(f"\n📋 Execution Log:")
                for log_entry in result['log']:
                    print(f"   {log_entry}")
            
            if result.get('success'):
                print(f"\n🎉 DEMO SUCCESS!")
                print(f"   ✅ All automation steps completed successfully")
                print(f"   ✅ Browser actions executed as programmed")
                print(f"   ✅ Form filling and navigation demonstrated")
                print(f"   ✅ AI-extracted steps can be automated!")
            else:
                print(f"\n⚠️ Demo completed with some issues:")
                print(f"   Error: {result.get('error', 'Unknown error')}")
                
        else:
            print(f"\n❌ Demo failed: HTTP {automation_response.status_code}")
            print(f"   Response: {automation_response.text}")
            
    except Exception as e:
        print(f"\n❌ Demo error: {e}")
        print(f"\n🔧 Troubleshooting:")
        print(f"   1. Make sure MCP server is running: cd MCP_server/MCP_mimic && python main.py")
        print(f"   2. Check that HEADLESS_BROWSER=False in .env")
        print(f"   3. Ensure Playwright is installed: pip install playwright")
        print(f"   4. Install browser: playwright install chromium")
    
    print(f"\n" + "="*60)
    print(f"🎬 BROWSER AUTOMATION DEMO COMPLETE")
    print(f"="*60)

def quick_automation_test():
    """Quick test to verify browser automation is working"""
    print("🧪 Quick Browser Automation Test")
    
    simple_steps = [
        {
            "action": "goto",
            "url": "https://example.com",
            "description": "Navigate to example.com"
        },
        {
            "action": "wait",
            "timeout": 3000,
            "description": "Wait 3 seconds"
        }
    ]
    
    try:
        response = requests.post(
            "http://localhost:8080/execute_browser_action",
            json={"steps": simple_steps, "video_id": "quick-test"},
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Quick test successful: {result.get('success')}")
            return True
        else:
            print(f"❌ Quick test failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Quick test error: {e}")
        return False

if __name__ == "__main__":
    print("🎬 MIMICKER AI - BROWSER AUTOMATION DEMO")
    print("🎯 Perfect for showing live automation to reviewers!")
    print()
    
    # Quick test first
    if quick_automation_test():
        print()
        input("Press Enter to start the full demo (browser will open)...")
        demo_browser_automation()
    else:
        print("\n🔧 Please fix the issues above before running the demo")
        print("Make sure:")
        print("1. MCP server is running")
        print("2. HEADLESS_BROWSER=False in MCP_server/MCP_mimic/.env")
        print("3. Playwright is installed and browsers are available")