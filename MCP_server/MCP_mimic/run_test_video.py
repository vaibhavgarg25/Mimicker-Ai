#!/usr/bin/env python3
"""
Run test_1.mp4 analysis and automation with visible browser
"""
import asyncio
import json
import os
from mcp_server import handle_call_tool

async def run_test_video_automation():
    """
    Run the complete workflow for test_1.mp4 with visible browser
    """
    print("🎬 Running test_1.mp4 Analysis & Automation")
    print("=" * 60)
    print("🖥️  Browser will be VISIBLE so you can watch the automation!")
    print("=" * 60)
    
    video_file = "test_1.mp4"
    
    # Check if video exists
    if not os.path.exists(video_file):
        print(f"❌ Video file not found: {video_file}")
        return
    
    try:
        # Step 1: Analyze the video
        print(f"\n🔍 Step 1: Analyzing {video_file}...")
        print("⏳ This may take a moment as we upload and process the video...")
        
        result = await handle_call_tool("analyze_video", {
            "video_url": video_file
        })
        
        analysis_data = json.loads(result[0].text)
        
        if "error" in analysis_data:
            print(f"❌ Analysis failed: {analysis_data['error']}")
            return
        
        print(f"✅ Video analysis completed!")
        print(f"📝 Video ID: {analysis_data.get('video_id')}")
        
        steps = analysis_data.get('steps', [])
        print(f"🎯 Extracted {len(steps)} automation steps:")
        print("-" * 50)
        
        for i, step in enumerate(steps, 1):
            action = step.get('action', 'unknown').upper()
            desc = step.get('description', 'No description')
            print(f"{i:2d}. {action:<8} - {desc}")
            
            # Show details
            if step.get('url'):
                print(f"     🌐 URL: {step['url']}")
            if step.get('selector'):
                print(f"     🎯 Selector: {step['selector']}")
            if step.get('text'):
                print(f"     ✏️  Text: '{step['text']}'")
        
        # Step 2: Execute with visible browser
        print(f"\n🚀 Step 2: Executing automation with VISIBLE browser...")
        print("👀 Watch your screen - a browser window will open!")
        print("⏱️  Each step will be executed with a small delay so you can see it")
        
        # Add small delays between steps for better visibility
        enhanced_steps = []
        for i, step in enumerate(steps):
            enhanced_steps.append(step)
            # Add a wait after each step (except the last one)
            if i < len(steps) - 1:
                enhanced_steps.append({
                    "action": "wait",
                    "timeout": 2000,  # 2 second pause
                    "description": f"Pause after step {i+1}"
                })
        
        print(f"🎬 Starting automation in 3 seconds...")
        await asyncio.sleep(3)
        
        exec_result = await handle_call_tool("execute_browser_action", {
            "steps": enhanced_steps,
            "video_id": analysis_data.get('video_id')
        })
        
        exec_data = json.loads(exec_result[0].text)
        
        print(f"\n📊 Automation Results:")
        print("=" * 50)
        
        if exec_data.get('success'):
            print(f"✅ SUCCESS! All steps completed successfully!")
        else:
            print(f"⚠️  PARTIAL SUCCESS - Stopped at step {exec_data.get('failed_step', 'unknown')}")
        
        print(f"🆔 Execution ID: {exec_data.get('execution_id')}")
        
        # Show execution log
        if exec_data.get('log'):
            print(f"\n📝 Step-by-step execution log:")
            for i, log_entry in enumerate(exec_data['log'], 1):
                print(f"  {i:2d}. {log_entry}")
        
        # Show error and AI suggestion if any
        if exec_data.get('error'):
            print(f"\n❌ Error encountered:")
            print(f"   {exec_data['error']}")
            
            # Get AI suggestion
            print(f"\n🤖 Getting AI suggestion for improvement...")
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
        
        print(f"\n🎉 Automation demo completed!")
        print(f"📊 You can view all your tasks and executions in the database")
        
    except Exception as e:
        print(f"💥 Error during automation: {e}")
        import traceback
        traceback.print_exc()

async def show_stats():
    """Show current system statistics"""
    print(f"\n📈 System Statistics:")
    print("-" * 30)
    
    # Get stats
    stats_result = await handle_call_tool("get_execution_stats", {})
    stats_data = json.loads(stats_result[0].text)
    
    print(f"Total executions: {stats_data.get('total_executions', 0)}")
    print(f"Success rate: {stats_data.get('success_rate', 0):.1f}%")
    print(f"Failed executions: {stats_data.get('failed_executions', 0)}")
    
    # Get recent activity
    activity_result = await handle_call_tool("get_recent_activity", {"limit": 3})
    activity_data = json.loads(activity_result[0].text)
    
    print(f"Recent videos analyzed: {len(activity_data.get('recent_videos', []))}")
    print(f"Recent executions: {len(activity_data.get('recent_executions', []))}")

if __name__ == "__main__":
    async def main():
        await run_test_video_automation()
        await show_stats()
    
    asyncio.run(main())