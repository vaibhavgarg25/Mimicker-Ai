#!/usr/bin/env python3
"""
Simple browser test for demo setup
"""

def test_browser():
    """Simple browser test without Unicode issues"""
    try:
        from playwright.sync_api import sync_playwright
        
        print("Testing browser automation...")
        
        with sync_playwright() as p:
            # Test with headless first
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto('https://example.com', timeout=10000)
            title = page.title()
            browser.close()
            
            print(f"SUCCESS: Browser test passed")
            print(f"Page title: {title}")
            return True
            
    except Exception as e:
        print(f"ERROR: Browser test failed: {e}")
        return False

def test_visible_browser():
    """Test visible browser mode"""
    try:
        from playwright.sync_api import sync_playwright
        
        print("Testing visible browser mode...")
        
        with sync_playwright() as p:
            # Test with visible browser
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()
            page.goto('https://example.com', timeout=10000)
            
            # Keep browser open for 3 seconds to show it's visible
            import time
            time.sleep(3)
            
            browser.close()
            
            print("SUCCESS: Visible browser test passed")
            return True
            
    except Exception as e:
        print(f"ERROR: Visible browser test failed: {e}")
        return False

if __name__ == "__main__":
    print("Browser Automation Test for Demo")
    print("=" * 40)
    
    # Test headless mode first
    if test_browser():
        print("\nTesting visible mode...")
        if test_visible_browser():
            print("\nALL TESTS PASSED!")
            print("Browser automation is ready for demo!")
        else:
            print("\nVisible browser test failed")
    else:
        print("\nBasic browser test failed")
        print("Please install Playwright browsers:")
        print("  python -m playwright install chromium")