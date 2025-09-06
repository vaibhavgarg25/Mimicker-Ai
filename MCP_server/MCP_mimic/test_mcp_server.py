#!/usr/bin/env python3
"""
Simple test script for MCP Browser Automation Server
"""
import json
import subprocess
import sys
import asyncio
from typing import Dict, Any

class MCPTester:
    def __init__(self, server_script: str = "mcp_server.py"):
        self.server_script = server_script
        self.process = None
    
    def start_server(self):
        """Start the MCP server process"""
        try:
            self.process = subprocess.Popen(
                [sys.executable, self.server_script],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=0
            )
            print("✅ Server started")
            return True
        except Exception as e:
            print(f"❌ Failed to start server: {e}")
            return False
    
    def send_request(self, method: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """Send a JSON-RPC request to the server"""
        if not self.process:
            raise Exception("Server not started")
        
        request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": method,
            "params": params or {}
        }
        
        request_json = json.dumps(request) + "\n"
        
        try:
            self.process.stdin.write(request_json)
            self.process.stdin.flush()
            
            response_line = self.process.stdout.readline()
            if response_line:
                return json.loads(response_line.strip())
            else:
                return {"error": "No response from server"}
                
        except Exception as e:
            return {"error": f"Communication error: {e}"}
    
    def test_initialization(self):
        """Test server initialization"""
        print("\n🔧 Testing server initialization...")
        
        # Send initialize request
        response = self.send_request("initialize", {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {
                "name": "test-client",
                "version": "1.0.0"
            }
        })
        
        print(f"Initialize response: {json.dumps(response, indent=2)}")
        return response
    
    def test_list_tools(self):
        """Test listing available tools"""
        print("\n🛠️  Testing list_tools...")
        
        response = self.send_request("tools/list")
        print(f"Tools response: {json.dumps(response, indent=2)}")
        
        if "result" in response and "tools" in response["result"]:
            tools = response["result"]["tools"]
            print(f"\n📋 Found {len(tools)} tools:")
            for tool in tools:
                print(f"  - {tool['name']}: {tool['description']}")
        
        return response
    
    def test_health_check(self):
        """Test the health_check tool"""
        print("\n🏥 Testing health_check tool...")
        
        response = self.send_request("tools/call", {
            "name": "health_check",
            "arguments": {}
        })
        
        print(f"Health check response: {json.dumps(response, indent=2)}")
        return response
    
    def test_get_tasks(self):
        """Test the get_tasks tool"""
        print("\n📝 Testing get_tasks tool...")
        
        response = self.send_request("tools/call", {
            "name": "get_tasks",
            "arguments": {}
        })
        
        print(f"Get tasks response: {json.dumps(response, indent=2)}")
        return response
    
    def test_invalid_tool(self):
        """Test calling an invalid tool"""
        print("\n❌ Testing invalid tool call...")
        
        response = self.send_request("tools/call", {
            "name": "nonexistent_tool",
            "arguments": {}
        })
        
        print(f"Invalid tool response: {json.dumps(response, indent=2)}")
        return response
    
    def cleanup(self):
        """Clean up the server process"""
        if self.process:
            self.process.terminate()
            self.process.wait()
            print("🧹 Server process cleaned up")

def main():
    """Run all tests"""
    print("🧪 Starting MCP Server Tests")
    print("=" * 50)
    
    tester = MCPTester()
    
    try:
        # Start server
        if not tester.start_server():
            return
        
        # Give server time to initialize
        import time
        time.sleep(2)
        
        # Run tests
        results = []
        
        # Test 1: Initialization
        init_result = tester.test_initialization()
        results.append(("initialization", init_result))
        
        # Test 2: List tools
        tools_result = tester.test_list_tools()
        results.append(("list_tools", tools_result))
        
        # Test 3: Health check
        health_result = tester.test_health_check()
        results.append(("health_check", health_result))
        
        # Test 4: Get tasks
        tasks_result = tester.test_get_tasks()
        results.append(("get_tasks", tasks_result))
        
        # Test 5: Invalid tool
        invalid_result = tester.test_invalid_tool()
        results.append(("invalid_tool", invalid_result))
        
        # Summary
        print("\n" + "=" * 50)
        print("🎯 Test Summary:")
        for test_name, result in results:
            status = "✅ PASS" if "error" not in result else "❌ FAIL"
            print(f"  {test_name}: {status}")
            if "error" in result:
                print(f"    Error: {result['error']}")
    
    except KeyboardInterrupt:
        print("\n⏹️  Tests interrupted by user")
    except Exception as e:
        print(f"\n💥 Test execution failed: {e}")
    finally:
        tester.cleanup()

if __name__ == "__main__":
    main()