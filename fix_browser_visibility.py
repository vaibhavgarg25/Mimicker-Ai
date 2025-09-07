#!/usr/bin/env python3
"""
Fix browser visibility issues
"""
import os
import subprocess
import sys

def fix_browser_visibility():
    print("🔧 FIXING BROWSER VISIBILITY ISSUES")
    print("=" * 50)
    
    print("🔍 Checking potential issues...")
    
    # Check 1: Windows Defender or Antivirus
    print("\n1. 🛡️ Antivirus/Security Software:")
    print("   - Windows Defender might be blocking browser automation")
    print("   - Some antivirus software blocks Playwright")
    print("   - Solution: Add Python.exe to antivirus exceptions")
    
    # Check 2: Multiple monitors
    print("\n2. 🖥️ Multiple Monitors:")
    print("   - Browser might open on a different monitor")
    print("   - Solution: Check all your screens")
    
    # Check 3: Browser installation
    print("\n3. 🌐 Browser Installation:")
    print("   - Checking if Chromium is properly installed...")
    
    try:
        # Try to find Playwright browsers
        import subprocess
        result = subprocess.run([sys.executable, "-m", "playwright", "install", "chromium"], 
                              capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            print("   ✅ Chromium installation successful")
        else:
            print("   ⚠️ Chromium installation had issues")
            print(f"   Output: {result.stdout}")
    except Exception as e:
        print(f"   ❌ Could not install Chromium: {e}")
    
    # Check 4: System permissions
    print("\n4. 🔐 System Permissions:")
    print("   - Python might need elevated permissions")
    print("   - Try running as administrator if needed")
    
    print("\n" + "=" * 50)
    print("🔧 RECOMMENDED FIXES:")
    print("=" * 50)
    
    print("\n🎯 Fix 1: Force Browser to Foreground")
    print("   I'll modify the browser automation to force visibility")
    
    print("\n🎯 Fix 2: Add Audio Alert")
    print("   I'll add a sound when browser opens")
    
    print("\n🎯 Fix 3: Add Desktop Notification")
    print("   I'll add a Windows notification when browser starts")
    
    print("\n🎯 Fix 4: Increase Browser Size")
    print("   I'll make the browser fullscreen and always on top")

if __name__ == "__main__":
    fix_browser_visibility()