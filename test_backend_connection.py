#!/usr/bin/env python3
"""
Test backend MCP connection
"""

import sys
import os
sys.path.append('backend')

from services.mcp_client import MCPClient

def test_backend_mcp():
    """Test if backend can connect to MCP server"""
    print("🧪 Testing Backend MCP Connection")
    
    # Initialize MCP client
    mcp_client = MCPClient()
    print(f"MCP Server URL: {mcp_client.mcp_base_url}")
    
    # Test health check
    print("\n📋 Testing MCP Health Check...")
    health = mcp_client.health_check()
    print(f"Health Check Result: {health}")
    
    if health:
        print("✅ Backend can connect to MCP server")
        
        # Test video analysis
        print("\n📋 Testing Video Analysis...")
        result = mcp_client.analyze_video("test_video.mp4")
        
        if result['success']:
            print("✅ Video analysis working")
            print(f"   Steps extracted: {len(result['data'].get('steps', []))}")
        else:
            print(f"❌ Video analysis failed: {result['error']}")
    else:
        print("❌ Backend cannot connect to MCP server")
        print("\n🔧 Troubleshooting:")
        print("   1. Make sure MCP server is running: cd MCP_server/MCP_mimic && python main.py")
        print("   2. Check MCP server is on port 8080")
        print("   3. Restart backend to pick up new .env settings")

if __name__ == "__main__":
    test_backend_mcp()