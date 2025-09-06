#!/usr/bin/env python3
"""
Analyze your test.mp4 video and run browser automation
"""
import asyncio
import json
import os
from mcp_server import handle_call_tool

async def analyze_and_automate_video(video_path: str):
    """
    Complete workflow: analyze local video -> extract steps -> execute automation
    """
    print("🎬 Video Analysis & Automation Workflow")
    print("=" * 60)
    
    # Check if video file exists
    if not os.path.exists(video_path):
        print(f"❌ Video file not found: {video_path}")
        print("📁 Current directory contents:")
        for item in os.listdir('.'):
            if item.endswith(('.mp4', '.avi', '.mov', '.mkv')):
                print(f"   📹 {item}")
        return
    
    print(f"📹 Found video file: {video_path}")
    print(f"📊 File size: {os.path.getsize(video_path) / (1024*1024):.1f} MB")
    
    try:
        # Step 1: Analyze the video
        print(f"\n🔍 Step 1: Analyzing video content...")
        result = await handle_call_tool("analyze_video", {
            "video_url": video_path  # Using local file path
        })
        
        analysis_data = json.loads(result[0].text)
        
        if "error" in analysis_data:
            print(f"❌ Analysis failed: {analysis_data['error']}")
            return
        
        print(f"✅ Analysis completed!")
        print(f"📝 Video ID: {analysis_data.get('video_id')}")
        print(f"🎯 Extracted {analysis_data.get('total_steps', 0)} automation steps")
        
        # Show the extracted steps
        steps = analysis_data.get('steps', [])
        if steps:
            print(f"\n📋 Extracted Automation Steps:")
            print("-" * 40)
            for i, step in enumerate(steps, 1):
                action = step.get('action', 'unknown')
                desc = step.get('description', 'No description')
                print(f"{i:2d}. {action.upper():<8} - {desc}")
                
                # Show key details
                if step.get('url'):
                    print(f"     URL: {step['url']}")
                if step.get('selector'):
                    print(f"     Selector: {step['selector']}")
                if step.get('text'):
                    print(f"     Text: '{step['text']}'")
                print()
        
        # Step 2: Ask user if they want to execute
        print("🤖 Step 2: Browser Automation")
        print("-" * 40)
        
        user_input = input("Do you want to execute these steps in the browser? (y/n): ").lower().strip()
        
        if user_input in ['y', 'yes']:
            print(f"\n🚀 Executing {len(steps)} automation steps...")
            
            # Execute the automation
            exec_result = await handle_call_tool("execute_browser_action", {
                "steps": steps,
                "video_id": analysis_data.get('video_id')
            })
            
            exec_data = json.loads(exec_result[0].text)
            
            print(f"\n📊 Execution Results:")
            print("-" * 40)
            print(f"Status: {'✅ SUCCESS' if exec_data.get('success') else '❌ FAILED'}")
            print(f"Execution ID: {exec_data.get('execution_id')}")
            
            if exec_data.get('log'):
                print(f"\n📝 Execution Log:")
                for i, log_entry in enumerate(exec_data['log'], 1):
                    print(f"  {i}. {log_entry}")
            
            if exec_data.get('error'):
                print(f"\n❌ Error: {exec_data['error']}")
                
                # Get AI suggestion for the error
                print(f"\n🤖 Getting AI suggestion...")
                suggestion_result = await handle_call_tool("fallback_llm", {
                    "error": exec_data['error'],
                    "context": {
                        "steps": steps,
                        "failed_step": exec_data.get('failed_step'),
                        "execution_id": exec_data.get('execution_id')
                    }
                })
                
                suggestion_data = json.loads(suggestion_result[0].text)
                if "error" not in suggestion_data:
                    print(f"💡 AI Suggestion:")
                    print(f"   {suggestion_data.get('suggestion', 'No suggestion available')}")
        
        else:
            print("⏭️  Skipping browser automation")
        
        print(f"\n✅ Workflow completed!")
        
    except Exception as e:
        print(f"💥 Workflow failed: {e}")
        import traceback
        traceback.print_exc()

async def list_video_files():
    """List available video files in current directory"""
    print("📁 Available video files:")
    video_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.webm']
    video_files = []
    
    for item in os.listdir('.'):
        if any(item.lower().endswith(ext) for ext in video_extensions):
            size_mb = os.path.getsize(item) / (1024*1024)
            print(f"   📹 {item} ({size_mb:.1f} MB)")
            video_files.append(item)
    
    if not video_files:
        print("   No video files found in current directory")
    
    return video_files

async def main():
    """Main function"""
    print("🎥 Video Analysis & Browser Automation Tool")
    print("=" * 60)
    
    # List available video files
    video_files = await list_video_files()
    
    # Check for test.mp4 specifically
    if "test.mp4" in video_files:
        print(f"\n✅ Found test.mp4!")
        await analyze_and_automate_video("test.mp4")
    else:
        print(f"\n❓ test.mp4 not found.")
        if video_files:
            print(f"Available videos: {', '.join(video_files)}")
            choice = input(f"Enter video filename to analyze (or 'q' to quit): ").strip()
            if choice and choice != 'q' and choice in video_files:
                await analyze_and_automate_video(choice)
        else:
            print("📝 To use this tool:")
            print("   1. Place your video file (test.mp4) in this directory")
            print("   2. Run this script again")
            print("   3. The AI will analyze your video and extract automation steps")
            print("   4. You can then execute those steps in a real browser")

if __name__ == "__main__":
    asyncio.run(main())