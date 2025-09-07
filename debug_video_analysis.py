#!/usr/bin/env python3
"""
Debug script to see exactly what steps are being extracted from your video
and compare with what should be extracted
"""

import os
import requests
import json
from datetime import datetime

MCP_SERVER_URL = "http://localhost:8080"
UPLOADS_DIR = "backend/uploads"

def find_latest_video():
    """Find the most recently uploaded video file"""
    if not os.path.exists(UPLOADS_DIR):
        print(f"❌ Uploads directory not found: {UPLOADS_DIR}")
        return None
    
    video_files = []
    for filename in os.listdir(UPLOADS_DIR):
        if filename.lower().endswith(('.mp4', '.mov', '.avi', '.mkv', '.webm')):
            filepath = os.path.join(UPLOADS_DIR, filename)
            mtime = os.path.getmtime(filepath)
            video_files.append((filepath, mtime, filename))
    
    if not video_files:
        print("❌ No video files found in uploads directory")
        return None
    
    # Sort by modification time (newest first)
    video_files.sort(key=lambda x: x[1], reverse=True)
    latest_video = video_files[0]
    
    print(f"📹 Latest video: {latest_video[2]}")
    print(f"📅 Upload time: {datetime.fromtimestamp(latest_video[1])}")
    return latest_video[0]

def analyze_video_detailed(video_path):
    """Analyze video and show detailed step extraction"""
    print(f"🧠 Analyzing video: {os.path.basename(video_path)}")
    print("=" * 50)
    
    try:
        payload = {
            'video_url': os.path.abspath(video_path)
        }
        
        response = requests.post(
            f"{MCP_SERVER_URL}/analyze_video",
            json=payload,
            timeout=120
        )
        
        if response.status_code == 200:
            data = response.json()
            steps = data.get('steps', [])
            video_id = data.get('video_id', 'unknown')
            
            print(f"✅ Analysis completed!")
            print(f"📊 Video ID: {video_id}")
            print(f"🎯 Extracted {len(steps)} steps:")
            print()
            
            # Show each step in detail
            for i, step in enumerate(steps, 1):
                action = step.get('action', 'unknown')
                description = step.get('description', 'No description')
                
                print(f"Step {i}: {action.upper()}")
                print(f"   Description: {description}")
                
                if action == 'goto':
                    url = step.get('url', 'No URL')
                    print(f"   URL: {url}")
                elif action == 'type':
                    selector = step.get('selector', 'No selector')
                    text = step.get('text', 'No text')
                    print(f"   Selector: {selector}")
                    print(f"   Text: '{text}'")
                elif action == 'click':
                    selector = step.get('selector', 'No selector')
                    print(f"   Selector: {selector}")
                elif action == 'wait':
                    timeout = step.get('timeout', 'No timeout')
                    print(f"   Timeout: {timeout}ms")
                elif action == 'scroll':
                    direction = step.get('direction', 'No direction')
                    amount = step.get('amount', 'No amount')
                    print(f"   Direction: {direction}")
                    print(f"   Amount: {amount}px")
                
                print()
            
            return steps, video_id
        else:
            print(f"❌ Analysis failed: {response.status_code} - {response.text}")
            return None, None
            
    except Exception as e:
        print(f"❌ Analysis error: {e}")
        return None, None

def test_extracted_steps(steps, video_id):
    """Test the extracted steps to see how they perform"""
    if not steps:
        print("❌ No steps to test")
        return False
    
    print("🧪 Testing extracted steps...")
    print("=" * 30)
    
    try:
        payload = {
            'steps': steps,
            'video_id': video_id
        }
        
        response = requests.post(
            f"{MCP_SERVER_URL}/execute_browser_action",
            json=payload,
            timeout=180
        )
        
        if response.status_code == 200:
            data = response.json()
            success = data.get('success', False)
            log = data.get('log', [])
            error = data.get('error')
            
            print(f"🎬 Execution {'SUCCESS' if success else 'FAILED'}!")
            print()
            
            if log:
                print("📋 Execution log:")
                for entry in log:
                    if "✓" in entry:
                        print(f"   ✅ {entry}")
                    elif "⚠️" in entry or "❌" in entry:
                        print(f"   ⚠️ {entry}")
                    else:
                        print(f"   📝 {entry}")
                print()
            
            if error:
                print(f"❌ Error: {error}")
                print()
            
            return success
        else:
            print(f"❌ Execution failed: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Execution error: {e}")
        return False

def compare_with_manual_description():
    """Ask user to describe what they expect vs what was extracted"""
    print("🤔 MANUAL COMPARISON")
    print("=" * 20)
    print("Please describe what actions your video shows:")
    print("(e.g., 'Opens Google, types yt, clicks search, clicks first result')")
    print()
    
    expected = input("What should the automation do? ").strip()
    
    if expected:
        print(f"\n📝 You expected: {expected}")
        print("\n💡 Compare this with the extracted steps above.")
        print("   Are the steps missing anything?")
        print("   Is the text content exactly what you typed?")
        print("   Are there extra steps that shouldn't be there?")
    
    return expected

def suggest_improvements(steps, expected_description):
    """Suggest improvements based on analysis"""
    print("\n🔧 IMPROVEMENT SUGGESTIONS")
    print("=" * 25)
    
    if not steps:
        print("❌ No steps were extracted - video analysis completely failed")
        return
    
    # Check for common issues
    has_goto = any(step.get('action') == 'goto' for step in steps)
    has_type = any(step.get('action') == 'type' for step in steps)
    has_click = any(step.get('action') == 'click' for step in steps)
    
    if not has_goto:
        print("⚠️ Missing navigation step - should start with 'goto' action")
    
    if not has_type and 'type' in expected_description.lower():
        print("⚠️ Missing typing step - video analysis didn't detect text input")
    
    if not has_click and 'click' in expected_description.lower():
        print("⚠️ Missing click step - video analysis didn't detect clicks")
    
    # Check text content
    type_steps = [step for step in steps if step.get('action') == 'type']
    if type_steps:
        print(f"\n📝 Text being typed:")
        for step in type_steps:
            text = step.get('text', '')
            print(f"   '{text}'")
        print("   ❓ Is this exactly what you typed in the video?")
    
    # Check sequence
    print(f"\n🔄 Action sequence:")
    for i, step in enumerate(steps, 1):
        action = step.get('action', 'unknown')
        desc = step.get('description', '')[:50] + '...' if len(step.get('description', '')) > 50 else step.get('description', '')
        print(f"   {i}. {action} - {desc}")
    print("   ❓ Is this the correct order of actions?")

def main():
    """Main debug function"""
    print("🔍 VIDEO ANALYSIS DEBUG TOOL")
    print("=" * 40)
    
    # Check MCP server
    try:
        response = requests.get(f"{MCP_SERVER_URL}/health", timeout=5)
        if response.status_code != 200:
            print("❌ MCP server is not running!")
            print("💡 Start it with: cd MCP_server/MCP_mimic && python main.py")
            return
    except:
        print("❌ MCP server is not running!")
        print("💡 Start it with: cd MCP_server/MCP_mimic && python main.py")
        return
    
    print("✅ MCP server is running")
    print()
    
    # Find latest video
    video_path = find_latest_video()
    if not video_path:
        return
    
    print()
    
    # Analyze video
    steps, video_id = analyze_video_detailed(video_path)
    
    if steps:
        # Test execution
        print("🎬 Ready to test the extracted steps!")
        choice = input("Test execution? (y/n): ").strip().lower()
        
        if choice.startswith('y'):
            test_extracted_steps(steps, video_id)
        
        # Manual comparison
        expected = compare_with_manual_description()
        
        # Suggestions
        suggest_improvements(steps, expected)
        
        print(f"\n🎯 SUMMARY:")
        print(f"   📹 Video: {os.path.basename(video_path)}")
        print(f"   📊 Steps extracted: {len(steps)}")
        print(f"   🎬 Ready for automation: {'Yes' if steps else 'No'}")
        
    else:
        print("❌ Video analysis failed completely")
        print("💡 This could be due to:")
        print("   - Video format not supported")
        print("   - Video too long or complex")
        print("   - Gemini API issues")
        print("   - Video content not clear enough")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n⏹️ Debug interrupted by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")