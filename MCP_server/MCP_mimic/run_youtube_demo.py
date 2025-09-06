#!/usr/bin/env python3
"""
YouTube automation demo with correct selectors
"""
import asyncio
import json
from mcp_server import handle_call_tool

async def run_youtube_demo():
    """
    Run a working YouTube automation demo
    """
    print("🎬 YouTube Automation Demo")
    print("=" * 50)
    print("🖥️  Browser will be VISIBLE - Watch the magic!")
    print("=" * 50)
    
    # Working YouTube automation steps
    demo_steps = [
        {
            "action": "goto",
            "url": "https://www.youtube.com",
            "description": "Navigate to YouTube"
        },
        {
            "action": "wait",
            "timeout": 3000,
            "description": "Wait for page load"
        },
        {
            "action": "click",
            "selector": "input[name='search_query']",  # Correct YouTube search selector
            "description": "Click search box"
        },
        {
            "action": "type",
            "selector": "input[name='search_query']",
            "text": "minecraft hardcore survival",
            "description": "Type search query"
        },
        {
            "action": "wait",
            "timeout": 1000,
            "description": "Brief pause"
        },
        {
            "action": "press",
            "key": "Enter",
            "description": "Press Enter to search"
        },
        {
            "action": "wait",
            "timeout": 4000,
            "description": "Wait for search results"
        },
        {
            "action": "click",
            "selector": "a#video-title",  # First video result
            "description": "Click first video"
        },
        {
            "action": "wait",
            "timeout": 3000,
            "description": "Wait for video to load"
        },
        {
            "action": "screenshot",
            "path": "youtube_automation_result.png",
            "description": "Take screenshot of result"
        }
    ]
    
    print(f"🎯 Demo Steps:")
    for i, step in enumerate(demo_steps, 1):
        action = step.get('action', 'unknown').upper()
        desc = step.get('description', 'No description')
        print(f"{i:2d}. {action:<12} - {desc}")
    
    print(f"\n🚀 Starting in 3 seconds...")
    print("👀 Watch your screen!")
    await asyncio.sleep(3)
    
    try:
        # Execute automation
        exec_result = await handle_call_tool("execute_browser_action", {
            "steps": demo_steps
        })
        
        exec_data = json.loads(exec_result[0].text)
        
        print(f"\n📊 Results:")
        print("=" * 30)
        
        if exec_data.get('success'):
            print(f"🎉 SUCCESS! All steps completed!")
        else:
            print(f"⚠️  Stopped at step {exec_data.get('failed_step', 'unknown')}")
        
        # Show what happened
        if exec_data.get('log'):
            print(f"\n📝 What happened:")
            for i, log_entry in enumerate(exec_data['log'], 1):
                print(f"  ✓ {log_entry}")
        
        if exec_data.get('error'):
            print(f"\n❌ Error: {exec_data['error']}")
        
        # Check if screenshot was taken
        import os
        if os.path.exists("youtube_automation_result.png"):
            print(f"\n📸 Screenshot saved: youtube_automation_result.png")
        
        print(f"\n✨ Demo completed!")
        
    except Exception as e:
        print(f"💥 Error: {e}")

async def show_video_analysis():
    """Show what the AI extracted from your video"""
    print(f"\n🤖 What AI Saw in Your Video:")
    print("-" * 40)
    
    result = await handle_call_tool("analyze_video", {"video_url": "test_1.mp4"})
    analysis_data = json.loads(result[0].text)
    
    if "error" not in analysis_data:
        steps = analysis_data.get('steps', [])
        print(f"📹 AI extracted these {len(steps)} steps:")
        for i, step in enumerate(steps, 1):
            action = step.get('action', 'unknown')
            desc = step.get('description', 'No description')
            print(f"  {i}. {action.upper()} - {desc}")
            if step.get('url'):
                print(f"     URL: {step['url']}")
            if step.get('selector'):
                print(f"     Selector: {step['selector']}")
            if step.get('text'):
                print(f"     Text: '{step['text']}'")

if __name__ == "__main__":
    async def main():
        await run_youtube_demo()
        await show_video_analysis()
    
    asyncio.run(main())