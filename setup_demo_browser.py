#!/usr/bin/env python3
"""
Setup browser automation for demo
Ensures Playwright browsers are installed and ready
"""

import subprocess
import sys
import os

def install_playwright_browsers():
    """Install Playwright browsers for demo"""
    print("🎬 Setting up Browser Automation for Demo")
    print("="*50)
    
    try:
        # Check if playwright is installed
        print("📋 Checking Playwright installation...")
        result = subprocess.run([sys.executable, "-c", "import playwright"], 
                              capture_output=True, text=True)
        
        if result.returncode != 0:
            print("❌ Playwright not installed")
            print("Installing Playwright...")
            subprocess.run([sys.executable, "-m", "pip", "install", "playwright"], check=True)
            print("✅ Playwright installed")
        else:
            print("✅ Playwright already installed")
        
        # Install browsers
        print("\n📋 Installing Chromium browser for automation...")
        try:
            subprocess.run([sys.executable, "-m", "playwright", "install", "chromium"], 
                         check=True, capture_output=True, text=True)
            print("✅ Chromium browser installed")
        except subprocess.CalledProcessError as e:
            print(f"⚠️ Browser installation warning: {e}")
            print("Trying alternative installation...")
            subprocess.run(["playwright", "install", "chromium"], check=True)
            print("✅ Chromium browser installed (alternative method)")
        
        # Verify installation
        print("\n📋 Verifying browser installation...")
        test_script = """
from playwright.sync_api import sync_playwright
try:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto('https://example.com')
        browser.close()
    print("✅ Browser test successful")
except Exception as e:
    print(f"❌ Browser test failed: {e}")
"""
        
        result = subprocess.run([sys.executable, "-c", test_script], 
                              capture_output=True, text=True)
        print(result.stdout)
        
        if "Browser test successful" in result.stdout:
            print("\n🎉 Browser automation setup complete!")
            print("✅ Ready for demo with visible browser")
            return True
        else:
            print(f"\n❌ Browser test failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Setup failed: {e}")
        return False

def configure_demo_mode():
    """Configure MCP server for demo mode (non-headless)"""
    print("\n📋 Configuring Demo Mode...")
    
    env_path = "MCP_server/MCP_mimic/.env"
    
    if os.path.exists(env_path):
        # Read current .env
        with open(env_path, 'r') as f:
            lines = f.readlines()
        
        # Update HEADLESS_BROWSER setting
        updated = False
        for i, line in enumerate(lines):
            if line.startswith('HEADLESS_BROWSER='):
                lines[i] = 'HEADLESS_BROWSER=False\n'
                updated = True
                break
        
        if not updated:
            lines.append('HEADLESS_BROWSER=False\n')
        
        # Write back
        with open(env_path, 'w') as f:
            f.writelines(lines)
        
        print("✅ Demo mode configured (HEADLESS_BROWSER=False)")
        return True
    else:
        print(f"❌ .env file not found at {env_path}")
        return False

def test_demo_setup():
    """Test the complete demo setup"""
    print("\n📋 Testing Demo Setup...")
    
    try:
        import requests
        
        # Test MCP server health
        response = requests.get("http://localhost:8080/health", timeout=5)
        if response.status_code == 200:
            print("✅ MCP server is running")
        else:
            print("❌ MCP server not responding")
            return False
        
        # Test simple automation
        test_payload = {
            "steps": [
                {"action": "goto", "url": "https://example.com", "description": "Test navigation"}
            ],
            "video_id": "setup-test"
        }
        
        response = requests.post("http://localhost:8080/execute_browser_action", 
                               json=test_payload, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print("✅ Browser automation test successful")
                return True
            else:
                print(f"❌ Browser automation test failed: {result.get('error')}")
                return False
        else:
            print(f"❌ Automation endpoint failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Demo test failed: {e}")
        return False

if __name__ == "__main__":
    print("🎬 MIMICKER AI - DEMO BROWSER SETUP")
    print("🎯 Preparing for project review with visible browser automation")
    print()
    
    success = True
    
    # Step 1: Install browsers
    if not install_playwright_browsers():
        success = False
    
    # Step 2: Configure demo mode
    if success and not configure_demo_mode():
        success = False
    
    # Step 3: Test setup (only if MCP server is running)
    if success:
        print("\n⚠️ Make sure MCP server is running for the test:")
        print("   cd MCP_server/MCP_mimic && python main.py")
        print()
        
        test_now = input("Test demo setup now? (y/n): ").lower().strip()
        if test_now == 'y':
            if test_demo_setup():
                print("\n🎉 DEMO SETUP COMPLETE!")
                print("✅ Browser automation ready for review")
                print("✅ Visible browser mode enabled")
                print("\n🚀 Ready to impress your reviewer!")
            else:
                print("\n⚠️ Demo test failed - check MCP server is running")
        else:
            print("\n✅ Setup complete - test when MCP server is running")
    
    if success:
        print(f"\n📋 Next Steps:")
        print(f"   1. Start MCP server: cd MCP_server/MCP_mimic && python main.py")
        print(f"   2. Run demo: python demo_browser_automation.py")
        print(f"   3. Show live browser automation to reviewer!")
    else:
        print(f"\n❌ Setup incomplete - please resolve issues above")