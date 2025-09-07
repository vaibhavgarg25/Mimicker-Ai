#!/usr/bin/env python3
"""
Complete Mimicker AI Workflow Demo
This script demonstrates the full integration between all components
"""

import requests
import json
import time
import os
from datetime import datetime

# Configuration
MCP_URL = "http://localhost:3000"
BACKEND_URL = "http://localhost:8000"

def print_header(title):
    """Print a formatted header"""
    print("\n" + "="*60)
    print(f"🎯 {title}")
    print("="*60)

def print_step(step_num, description):
    """Print a formatted step"""
    print(f"\n📋 Step {step_num}: {description}")
    print("-" * 40)

def test_mcp_analysis():
    """Test MCP server video analysis"""
    print_step(1, "Testing MCP Video Analysis")
    
    # Test with sample video
    test_payload = {
        "video_url": "sample_tutorial_video.mp4"  # This will use fallback steps
    }
    
    try:
        response = requests.post(f"{MCP_URL}/analyze_video", json=test_payload, timeout=30)
        if response.status_code == 200:
            data = response.json()
            steps = data.get('steps', [])
            video_id = data.get('video_id', 'demo-video-123')
            
            print(f"✅ Analysis successful!")
            print(f"   📊 Extracted {len(steps)} automation steps")
            print(f"   🆔 Video ID: {video_id}")
            
            # Show first few steps
            print(f"\n📝 Sample Steps:")
            for i, step in enumerate(steps[:3], 1):
                print(f"   {i}. {step.get('action', 'unknown')} - {step.get('description', 'No description')}")
            
            return {'success': True, 'video_id': video_id, 'steps': steps}
        else:
            print(f"❌ Analysis failed: {response.status_code} - {response.text}")
            return {'success': False}
    except Exception as e:
        print(f"❌ Analysis error: {e}")
        return {'success': False}

def test_browser_automation(steps, video_id):
    """Test browser automation execution"""
    print_step(2, "Testing Browser Automation")
    
    automation_payload = {
        'steps': steps,
        'video_id': video_id
    }
    
    try:
        response = requests.post(f"{MCP_URL}/execute_browser_action", json=automation_payload, timeout=60)
        if response.status_code == 200:
            data = response.json()
            success = data.get('success', False)
            log = data.get('log', [])
            
            print(f"✅ Automation {'completed' if success else 'failed'}!")
            print(f"   📋 Execution ID: {data.get('execution_id', 'N/A')}")
            
            if log:
                print(f"\n📄 Execution Log:")
                for entry in log[-5:]:  # Show last 5 log entries
                    print(f"   • {entry}")
            
            if not success and data.get('error'):
                print(f"   ⚠️ Error: {data.get('error')}")
            
            return {'success': success, 'data': data}
        else:
            print(f"❌ Automation failed: {response.status_code} - {response.text}")
            return {'success': False}
    except Exception as e:
        print(f"❌ Automation error: {e}")
        return {'success': False}

def test_complete_workflow():
    """Test the complete workflow: analyze + execute"""
    print_step(3, "Testing Complete Workflow")
    
    workflow_payload = {
        "video_url": "complete_workflow_demo.mp4"
    }
    
    try:
        response = requests.post(f"{MCP_URL}/run_task_from_video", json=workflow_payload, timeout=120)
        if response.status_code == 200:
            data = response.json()
            
            print(f"✅ Complete workflow finished!")
            print(f"   📊 Status: {data.get('status', 'unknown')}")
            print(f"   🆔 Video ID: {data.get('video_id', 'N/A')}")
            print(f"   🔧 Execution ID: {data.get('execution_id', 'N/A')}")
            
            if data.get('log'):
                print(f"\n📄 Final Log:")
                for entry in data.get('log', [])[-3:]:  # Show last 3 entries
                    print(f"   • {entry}")
            
            if data.get('suggestion'):
                print(f"\n💡 AI Suggestion: {data.get('suggestion')}")
            
            return {'success': True, 'data': data}
        else:
            print(f"❌ Workflow failed: {response.status_code} - {response.text}")
            return {'success': False}
    except Exception as e:
        print(f"❌ Workflow error: {e}")
        return {'success': False}

def show_integration_summary():
    """Show what the integration provides"""
    print_header("🚀 Mimicker AI Integration Summary")
    
    features = [
        "✅ Automatic video analysis after upload",
        "✅ AI-powered step extraction using Gemini",
        "✅ Browser automation with Playwright", 
        "✅ Real-time status tracking",
        "✅ Error handling and AI suggestions",
        "✅ Complete workflow orchestration",
        "✅ User authentication and video management",
        "✅ RESTful API for all operations"
    ]
    
    print("\n🎯 Key Features:")
    for feature in features:
        print(f"   {feature}")
    
    print(f"\n🌐 Service Endpoints:")
    print(f"   • Frontend: http://localhost:3000 (Next.js)")
    print(f"   • Backend API: http://localhost:8000 (Flask)")
    print(f"   • MCP Server: http://localhost:3000 (Video Analysis)")
    
    print(f"\n📱 User Workflow:")
    workflow_steps = [
        "1. Upload video via web interface",
        "2. System automatically analyzes video",
        "3. View extracted steps in dashboard", 
        "4. Trigger browser automation",
        "5. Monitor real-time execution",
        "6. Get AI suggestions for failures"
    ]
    
    for step in workflow_steps:
        print(f"   {step}")

def main():
    """Run the complete demo"""
    print_header("🎬 Mimicker AI Complete Integration Demo")
    print(f"⏰ Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Test individual components
    analysis_result = test_mcp_analysis()
    
    if analysis_result['success']:
        automation_result = test_browser_automation(
            analysis_result['steps'], 
            analysis_result['video_id']
        )
    
    # Test complete workflow
    workflow_result = test_complete_workflow()
    
    # Show summary
    show_integration_summary()
    
    # Final results
    print_header("📊 Demo Results")
    
    results = [
        ("Video Analysis", analysis_result.get('success', False)),
        ("Browser Automation", automation_result.get('success', False) if 'automation_result' in locals() else False),
        ("Complete Workflow", workflow_result.get('success', False))
    ]
    
    passed = sum(1 for _, success in results if success)
    
    print(f"\n🎯 Test Results:")
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"   {status} - {test_name}")
    
    print(f"\n📈 Overall: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print(f"\n🎉 All systems working! Your Mimicker AI integration is ready!")
        print(f"\n🚀 Next Steps:")
        print(f"   1. Start the backend: cd backend && python app.py")
        print(f"   2. Start the frontend: cd client && npm run dev")
        print(f"   3. Open http://localhost:3000 in your browser")
        print(f"   4. Sign up and upload a video to test the full workflow")
    else:
        print(f"\n⚠️ Some components need attention. Check the logs above.")
    
    print(f"\n⏰ Demo completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()