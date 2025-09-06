#!/usr/bin/env python3
"""
Interactive MCP Client for Browser Automation Server
"""
import asyncio
import json
from mcp_server import handle_list_tools, handle_call_tool

class MCPClient:
    def __init__(self):
        self.tools = []
    
    async def initialize(self):
        """Initialize the client and get available tools"""
        print("🚀 Initializing MCP Client...")
        self.tools = await handle_list_tools()
        print(f"✅ Connected! Found {len(self.tools)} available tools")
    
    def show_tools(self):
        """Display available tools"""
        print("\n📋 Available Tools:")
        print("-" * 50)
        for i, tool in enumerate(self.tools, 1):
            print(f"{i}. {tool.name}")
            print(f"   {tool.description}")
            print()
    
    async def call_tool(self, tool_name: str, arguments: dict = None):
        """Call a specific tool"""
        if arguments is None:
            arguments = {}
        
        print(f"\n🔧 Calling tool: {tool_name}")
        print(f"📝 Arguments: {json.dumps(arguments, indent=2)}")
        
        try:
            result = await handle_call_tool(tool_name, arguments)
            response_data = json.loads(result[0].text)
            
            print(f"✅ Tool executed successfully!")
            print(f"📊 Response: {json.dumps(response_data, indent=2)}")
            return response_data
            
        except Exception as e:
            print(f"❌ Tool execution failed: {e}")
            return {"error": str(e)}
    
    async def interactive_mode(self):
        """Run interactive mode"""
        print("\n🎮 Interactive Mode - Type 'help' for commands")
        print("-" * 50)
        
        while True:
            try:
                command = input("\n> ").strip().lower()
                
                if command == 'help':
                    print("\nAvailable commands:")
                    print("  help - Show this help")
                    print("  tools - List available tools")
                    print("  health - Check system health")
                    print("  tasks - Get all tasks")
                    print("  analyze <url> - Analyze a video URL")
                    print("  run <url> - Run complete workflow for video URL")
                    print("  quit - Exit")
                
                elif command == 'tools':
                    self.show_tools()
                
                elif command == 'health':
                    await self.call_tool("health_check")
                
                elif command == 'tasks':
                    await self.call_tool("get_tasks")
                
                elif command.startswith('analyze '):
                    url = command[8:].strip()
                    if url:
                        await self.call_tool("analyze_video", {"video_url": url})
                    else:
                        print("❌ Please provide a video URL")
                
                elif command.startswith('run '):
                    url = command[4:].strip()
                    if url:
                        await self.call_tool("run_task_from_video", {"video_url": url})
                    else:
                        print("❌ Please provide a video URL")
                
                elif command == 'quit':
                    print("👋 Goodbye!")
                    break
                
                else:
                    print("❓ Unknown command. Type 'help' for available commands.")
            
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except EOFError:
                print("\n👋 Goodbye!")
                break

async def main():
    """Main function"""
    client = MCPClient()
    await client.initialize()
    
    # Show available tools
    client.show_tools()
    
    # Quick demo
    print("\n🎯 Quick Demo:")
    print("1. Checking system health...")
    await client.call_tool("health_check")
    
    print("\n2. Getting current tasks...")
    await client.call_tool("get_tasks")
    
    # Start interactive mode
    await client.interactive_mode()

if __name__ == "__main__":
    asyncio.run(main())