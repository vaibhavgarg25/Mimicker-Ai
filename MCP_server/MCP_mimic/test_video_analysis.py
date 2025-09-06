#!/usr/bin/env python3
"""
Test video analysis functionality
"""
import asyncio
import json
from mcp_server import handle_call_tool

async def test_video_analysis():
    """Test the video analysis workflow"""
    print("🧪 Testing Video Analysis Workflow")
    print("=" * 50)
    
    # Test 1: Check if system is ready
    print("\n1. 🏥 System Health Check:")
    health = await handle_call_tool("health_check", {})
    health_data = json.loads(health[0].text)
    print(f"   Status: {health_data.get('status')}")
    print(f"   Gemini API: {health_data.get('services', {}).get('video_analyzer')}")
    
    # Test 2: Test with a sample "video" (will use fallback)
    print("\n2. 📹 Testing Video Analysis (Sample):")
    result = await handle_call_tool("analyze_video", {
        "video_url": "test_1.mp4"
    })
    
    analysis_data = json.loads(result[0].text)
    
    if "error" not in analysis_data:
        print(f"   ✅ Analysis successful!")
        print(f"   Video ID: {analysis_data.get('video_id')}")
        print(f"   Steps: {analysis_data.get('total_steps')}")
        
        steps = analysis_data.get('steps', [])
        if steps:
            print(f"\n   📋 Sample Steps:")
            for i, step in enumerate(steps[:3], 1):  # Show first 3
                print(f"     {i}. {step.get('action')} - {step.get('description', 'N/A')}")
            if len(steps) > 3:
                print(f"     ... and {len(steps) - 3} more steps")
    else:
        print(f"   ❌ Analysis failed: {analysis_data.get('error')}")
    
    # Test 3: Test complete workflow
    print("\n3. 🔄 Testing Complete Workflow:")
    workflow_result = await handle_call_tool("run_task_from_video", {
        "video_url": "demo_video.mp4"
    })
    
    workflow_data = json.loads(workflow_result[0].text)
    print(f"   Status: {workflow_data.get('status')}")
    print(f"   Total Steps: {workflow_data.get('total_steps', 0)}")
    
    if workflow_data.get('error'):
        print(f"   Error: {workflow_data['error']}")
        if workflow_data.get('suggestion'):
            print(f"   AI Suggestion: {workflow_data['suggestion'][:100]}...")
    
    print(f"\n✅ Testing completed!")

if __name__ == "__main__":
    asyncio.run(test_video_analysis())