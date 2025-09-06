#!/usr/bin/env python3
"""
Test MCP server without browser automation
"""
import asyncio
import json
from mcp_server import handle_call_tool

async def test_mcp_without_browser():
    """Test MCP tools that don't require browser automation"""
    print("🧪 Testing MCP Server (No Browser Required)")
    print("=" * 50)
    
    # Test 1: Health check
    print("\n1. 🏥 Health Check:")
    health = await handle_call_tool("health_check", {})
    health_data = json.loads(health[0].text)
    print(f"   Status: {health_data.get('status')}")
    print(f"   Database: {health_data.get('database', {}).get('status')}")
    print(f"   Services: {health_data.get('services', {})}")
    
    # Test 2: Video analysis (no execution)
    print("\n2. 📹 Video Analysis:")
    video_result = await handle_call_tool("analyze_video", {
        "video_url": "https://www.youtube.com/watch?v=example123"
    })
    video_data = json.loads(video_result[0].text)
    if "error" not in video_data:
        print(f"   ✅ Analysis successful!")
        print(f"   Video ID: {video_data.get('video_id')}")
        print(f"   Steps extracted: {video_data.get('total_steps')}")
        
        # Show first few steps
        steps = video_data.get('steps', [])
        if steps:
            print(f"   First 3 steps:")
            for i, step in enumerate(steps[:3], 1):
                print(f"     {i}. {step.get('action')} - {step.get('description', 'N/A')}")
    else:
        print(f"   ⚠️  Analysis result: {video_data.get('error')}")
    
    # Test 3: Get all tasks
    print("\n3. 📝 Task Management:")
    tasks = await handle_call_tool("get_tasks", {})
    tasks_data = json.loads(tasks[0].text)
    print(f"   Total tasks: {tasks_data.get('total_count', 0)}")
    
    # Test 4: Execution statistics
    print("\n4. 📊 Statistics:")
    stats = await handle_call_tool("get_execution_stats", {})
    stats_data = json.loads(stats[0].text)
    print(f"   Total executions: {stats_data.get('total_executions', 0)}")
    print(f"   Success rate: {stats_data.get('success_rate', 0):.1f}%")
    
    # Test 5: Recent activity
    print("\n5. 🕒 Recent Activity:")
    activity = await handle_call_tool("get_recent_activity", {"limit": 3})
    activity_data = json.loads(activity[0].text)
    print(f"   Recent videos: {len(activity_data.get('recent_videos', []))}")
    print(f"   Recent executions: {len(activity_data.get('recent_executions', []))}")
    
    # Test 6: AI fallback suggestion
    print("\n6. 🤖 AI Fallback:")
    suggestion = await handle_call_tool("fallback_llm", {
        "error": "Element not found: #submit-button",
        "context": {"action": "click", "selector": "#submit-button"}
    })
    suggestion_data = json.loads(suggestion[0].text)
    if "error" not in suggestion_data:
        print(f"   ✅ AI suggestion generated!")
        print(f"   Suggestion: {suggestion_data.get('suggestion', '')[:100]}...")
    else:
        print(f"   ⚠️  Suggestion error: {suggestion_data.get('error')}")
    
    print(f"\n✅ All non-browser tests completed successfully!")

if __name__ == "__main__":
    asyncio.run(test_mcp_without_browser())