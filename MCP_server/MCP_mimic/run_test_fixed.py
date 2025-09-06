#!/usr/bin/env python3
"""
Run test_1.mp4 with corrected automation steps
"""
import asyncio
import json
import os
from mcp_server import handle_call_tool

async def run_corrected_automation():
    """
    Run automation with manually corrected steps based on the video analysis
    """
    print("🎬 Running Corrected Automation for test_1.mp4")
    print("=" * 60)
    print("🖥️  Browser will be VISIBLE - Watch the automation!")
    print("=" * 60)
    
    # Based on the video analysis, here are the corrected steps
    corrected_steps = [
        {
            "action": "goto",
            "url": "https://www.youtube.com",  # Fixed: proper URL
            "description": "Navigate to YouTube homepage"
        },
        {
            "action": "wait",
            "timeout": 3000,
            "description": "Wait for page to load"
        },
        {
            "action": "click",
            "selector": "input#search",  # YouTube search box
            "description": "Click on the search bar"
        },
        {
            "action": "type",
            "selector": "input#search",
            "text": "minecraft hardcore 1000 days",
            "description": "Type search query"
        },
        {
            "action": "press",
            "key": "Enter",
            "description": "Press Enter to search"
        },
        {
            "action": "wait",
            "timeout": 3000,
            "description": "Wait for search results"
        },
        {
            "action": "click",
            "selector": "a#video-title[href*='watch']",  # First video result
            "description": "Click on the first video result"
        }
    ]
    
    print(f"🎯 Executing {len(corrected_steps)} corrected automation steps:")
    print("-" * 50)
    
    for i, step in enumerate(corrected_steps, 1):
        action = step.get('action', 'unknown').upper()
        desc = step.get('description', 'No description')
        print(f"{i:2d}. {action:<8} - {desc}")
        
        if step.get('url'):
            print(f"     🌐 URL: {step['url']}")
        if step.get('selector'):
            print(f"     🎯 Selector: {step['selector']}")
        if step.get('text'):
            print(f"     ✏️  Text: '{step['text']}'")
        if step.get('key'):
            print(f"     ⌨️  Key: {step['key']}")
    
    print(f"\n🚀 Starting automation in 3 seconds...")
    print("👀 Watch your screen - browser window will open!")
    await asyncio.sleep(3)
    
    try:
        # Execute the corrected automation
        exec_result = await handle_call_tool("execute_browser_action", {
            "steps": corrected_steps
        })
        
        exec_data = json.loads(exec_result[0].text)
        
        print(f"\n📊 Automation Results:")
        print("=" * 50)
        
        if exec_data.get('success'):
            print(f"✅ SUCCESS! All steps completed successfully!")
        else:
            print(f"⚠️  STOPPED at step {exec_data.get('failed_step', 'unknown')}")
        
        print(f"🆔 Execution ID: {exec_data.get('execution_id')}")
        
        # Show execution log
        if exec_data.get('log'):
            print(f"\n📝 Execution log:")
            for i, log_entry in enumerate(exec_data['log'], 1):
                print(f"  {i:2d}. {log_entry}")
        
        # Show error if any
        if exec_data.get('error'):
            print(f"\n❌ Error: {exec_data['error']}")
            
            # Get AI suggestion
            print(f"\n🤖 AI Suggestion:")
            suggestion_result = await handle_call_tool("fallback_llm", {
                "error": exec_data['error'],
                "context": {"steps": corrected_steps, "failed_step": exec_data.get('failed_step')}
            })
            
            suggestion_data = json.loads(suggestion_result[0].text)
            if "error" not in suggestion_data:
                print(f"💡 {suggestion_data.get('suggestion', 'No suggestion available')}")
        
        print(f"\n🎉 Demo completed!")
        
    except Exception as e:
        print(f"💥 Error: {e}")
        import traceback
        traceback.print_exc()

async def run_original_analysis():
    """
    Also run the original video analysis to compare
    """
    print(f"\n🔍 Original Video Analysis Results:")
    print("-" * 40)
    
    result = await handle_call_tool("analyze_video", {"video_url": "test_1.mp4"})
    analysis_data = json.loads(result[0].text)
    
    if "error" not in analysis_data:
        steps = analysis_data.get('steps', [])
        print(f"📹 AI extracted {len(steps)} steps from your video:")
        for i, step in enumerate(steps, 1):
            print(f"  {i}. {step.get('action')} - {step.get('description', 'N/A')}")

if __name__ == "__main__":
    async def main():
        await run_corrected_automation()
        await run_original_analysis()
    
    asyncio.run(main())