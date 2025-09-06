#!/usr/bin/env python3
"""
Test the complete MCP workflow
"""
import asyncio
import json
from mcp_server import handle_call_tool

async def test_complete_workflow():
    """Test the complete video-to-automation workflow"""
    print("🎬 Testing Complete MCP Workflow")
    print("=" * 50)
    
    # Test with a sample video URL
    video_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    
    print(f"📹 Processing video: {video_url}")
    
    # Run the complete workflow
    result = await handle_call_tool("run_task_from_video", {
        "video_url": video_url
    })
    
    response_data = json.loads(result[0].text)
    
    print(f"\n📊 Workflow Results:")
    print(f"Status: {response_data.get('status', 'unknown')}")
    print(f"Video ID: {response_data.get('video_id', 'N/A')}")
    print(f"Execution ID: {response_data.get('execution_id', 'N/A')}")
    print(f"Total Steps: {response_data.get('total_steps', 0)}")
    
    if response_data.get('error'):
        print(f"❌ Error: {response_data['error']}")
        if response_data.get('suggestion'):
            print(f"💡 AI Suggestion: {response_data['suggestion']}")
    
    if response_data.get('log'):
        print(f"\n📝 Execution Log:")
        for i, log_entry in enumerate(response_data['log'], 1):
            print(f"  {i}. {log_entry}")
    
    return response_data

async def test_individual_tools():
    """Test individual MCP tools"""
    print("\n🔧 Testing Individual Tools")
    print("=" * 50)
    
    # 1. Health check
    print("\n1. Health Check:")
    health = await handle_call_tool("health_check", {})
    health_data = json.loads(health[0].text)
    print(f"   Status: {health_data.get('status', 'unknown')}")
    
    # 2. Get execution stats
    print("\n2. Execution Statistics:")
    stats = await handle_call_tool("get_execution_stats", {})
    stats_data = json.loads(stats[0].text)
    print(f"   Total executions: {stats_data.get('total_executions', 0)}")
    print(f"   Success rate: {stats_data.get('success_rate', 0)}%")
    
    # 3. Recent activity
    print("\n3. Recent Activity:")
    activity = await handle_call_tool("get_recent_activity", {"limit": 5})
    activity_data = json.loads(activity[0].text)
    print(f"   Recent videos: {len(activity_data.get('recent_videos', []))}")
    print(f"   Recent executions: {len(activity_data.get('recent_executions', []))}")

if __name__ == "__main__":
    async def main():
        await test_complete_workflow()
        await test_individual_tools()
        print("\n✅ All tests completed!")
    
    asyncio.run(main())