#!/usr/bin/env python3
"""
Simple MCP server test using direct imports
"""
import asyncio
import json
from mcp_server import server, handle_list_tools, handle_call_tool

async def test_mcp_server():
    """Test MCP server functionality directly"""
    print("🧪 Testing MCP Server Components")
    print("=" * 50)
    
    try:
        # Test 1: List tools
        print("\n🛠️  Testing list_tools...")
        tools = await handle_list_tools()
        print(f"✅ Found {len(tools)} tools:")
        for tool in tools:
            print(f"  - {tool.name}: {tool.description}")
        
        # Test 2: Health check
        print("\n🏥 Testing health_check tool...")
        health_result = await handle_call_tool("health_check", {})
        health_data = json.loads(health_result[0].text)
        print(f"Health status: {health_data.get('status', 'unknown')}")
        
        # Test 3: Get tasks
        print("\n📝 Testing get_tasks tool...")
        tasks_result = await handle_call_tool("get_tasks", {})
        tasks_data = json.loads(tasks_result[0].text)
        print(f"Tasks count: {tasks_data.get('total_count', 0)}")
        
        # Test 4: Analyze video (with example URL)
        print("\n📹 Testing analyze_video tool...")
        video_result = await handle_call_tool("analyze_video", {
            "video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        })
        video_data = json.loads(video_result[0].text)
        if "error" not in video_data:
            print(f"✅ Video analyzed successfully, {video_data.get('total_steps', 0)} steps extracted")
        else:
            print(f"⚠️  Video analysis result: {video_data.get('error', 'Unknown error')}")
        
        print("\n✅ All tests completed successfully!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_mcp_server())