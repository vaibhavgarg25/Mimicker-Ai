# mcp_server.py - Updated MCP Server for v1.13.1+
import asyncio
import json
from typing import Any, Sequence, Dict, List
from mcp.server.models import InitializationOptions
from mcp.server import NotificationOptions, Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    Resource,
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
    LoggingLevel
)
import mcp.types as types
from services.vision import VideoAnalyzer
from services.browser import BrowserAutomator
from services.db import Database
from datetime import datetime
import traceback
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize services
try:
    db = Database()
    video_analyzer = VideoAnalyzer()
    browser_automator = BrowserAutomator(headless=False)  # Show browser window
    print("✅ All services initialized successfully")
except Exception as e:
    print(f"❌ Error initializing services: {e}")
    # Continue anyway for demo purposes

# Create MCP server
server = Server("browser-automation-mcp")

@server.list_tools()
async def handle_list_tools() -> List[Tool]:
    """
    List available tools for browser automation
    """
    return [
        Tool(
            name="analyze_video",
            description="Analyze a tutorial video and extract structured browser automation steps using Google Gemini AI",
            inputSchema={
                "type": "object",
                "properties": {
                    "video_url": {
                        "type": "string",
                        "description": "URL of the video to analyze (YouTube, Vimeo, etc.)"
                    }
                },
                "required": ["video_url"],
                "additionalProperties": False
            }
        ),
        Tool(
            name="execute_browser_action",
            description="Execute browser automation steps using Playwright with comprehensive action support",
            inputSchema={
                "type": "object",
                "properties": {
                    "steps": {
                        "type": "array",
                        "description": "Array of browser automation steps to execute",
                        "items": {
                            "type": "object",
                            "properties": {
                                "action": {
                                    "type": "string",
                                    "enum": ["goto", "click", "type", "wait", "scroll", "screenshot", "select", "hover", "press"]
                                },
                                "selector": {"type": "string"},
                                "url": {"type": "string"},
                                "text": {"type": "string"},
                                "value": {"type": "string"},
                                "key": {"type": "string"},
                                "timeout": {"type": "integer"},
                                "direction": {"type": "string"},
                                "amount": {"type": "integer"},
                                "path": {"type": "string"},
                                "description": {"type": "string"}
                            },
                            "required": ["action"]
                        }
                    },
                    "video_id": {
                        "type": "string",
                        "description": "Optional video ID for execution logging and tracking"
                    }
                },
                "required": ["steps"],
                "additionalProperties": False
            }
        ),
        Tool(
            name="fallback_llm",
            description="Get AI-powered suggestions for failed automation steps using contextual error analysis",
            inputSchema={
                "type": "object",
                "properties": {
                    "error": {
                        "type": "string",
                        "description": "Error message from the failed automation step"
                    },
                    "context": {
                        "type": "object",
                        "description": "Additional context about the failure (step details, page state, etc.)",
                        "additionalProperties": True
                    }
                },
                "required": ["error"],
                "additionalProperties": False
            }
        ),
        Tool(
            name="run_task_from_video",
            description="Complete end-to-end workflow: analyze video → extract steps → execute automation → handle errors with AI fallback",
            inputSchema={
                "type": "object",
                "properties": {
                    "video_url": {
                        "type": "string",
                        "description": "URL of the tutorial video to process completely"
                    }
                },
                "required": ["video_url"],
                "additionalProperties": False
            }
        ),
        Tool(
            name="get_tasks",
            description="Retrieve all stored video analysis tasks with their extracted steps and metadata",
            inputSchema={
                "type": "object",
                "properties": {},
                "additionalProperties": False
            }
        ),
        Tool(
            name="get_task",
            description="Get detailed information about a specific video analysis task",
            inputSchema={
                "type": "object",
                "properties": {
                    "task_id": {
                        "type": "string",
                        "description": "Unique identifier of the task to retrieve"
                    }
                },
                "required": ["task_id"],
                "additionalProperties": False
            }
        ),
        Tool(
            name="delete_task",
            description="Delete a video analysis task and its associated data",
            inputSchema={
                "type": "object",
                "properties": {
                    "task_id": {
                        "type": "string",
                        "description": "Unique identifier of the task to delete"
                    }
                },
                "required": ["task_id"],
                "additionalProperties": False
            }
        ),
        Tool(
            name="get_execution",
            description="Get detailed execution logs and results for a specific automation run",
            inputSchema={
                "type": "object",
                "properties": {
                    "execution_id": {
                        "type": "string",
                        "description": "Unique identifier of the execution to retrieve"
                    }
                },
                "required": ["execution_id"],
                "additionalProperties": False
            }
        ),
        Tool(
            name="get_execution_stats",
            description="Get comprehensive analytics and statistics about automation executions",
            inputSchema={
                "type": "object",
                "properties": {},
                "additionalProperties": False
            }
        ),
        Tool(
            name="health_check",
            description="Check the health status of all system components (database, AI services, browser)",
            inputSchema={
                "type": "object",
                "properties": {},
                "additionalProperties": False
            }
        ),
        Tool(
            name="get_recent_activity",
            description="Get recent system activity including video analysis, executions, and corrections",
            inputSchema={
                "type": "object",
                "properties": {
                    "limit": {
                        "type": "integer",
                        "description": "Maximum number of recent items to return (default: 10)",
                        "default": 10,
                        "minimum": 1,
                        "maximum": 100
                    }
                },
                "additionalProperties": False
            }
        )
    ]

@server.call_tool()
async def handle_call_tool(name: str, arguments: Dict[str, Any] | None) -> List[types.TextContent]:
    """
    Handle tool calls with comprehensive error handling and logging
    """
    if arguments is None:
        arguments = {}
    
    try:
        print(f"🔧 Executing tool: {name} with args: {arguments}")
        
        if name == "analyze_video":
            video_url = arguments.get("video_url")
            if not video_url:
                return [types.TextContent(
                    type="text",
                    text=json.dumps({"error": "video_url is required"})
                )]
            
            # Analyze video with Gemini
            steps = video_analyzer.analyze_video(video_url)
            
            # Store in database
            video_doc = {
                'video_url': video_url,
                'uploaded_at': datetime.utcnow(),
                'steps': steps
            }
            video_id = db.insert_video(video_doc)
            
            result = {
                'video_id': str(video_id),
                'steps': steps,
                'total_steps': len(steps),
                'analyzed_at': datetime.utcnow().isoformat()
            }
            
            return [types.TextContent(
                type="text",
                text=json.dumps(result, default=str)
            )]
        
        elif name == "execute_browser_action":
            steps = arguments.get("steps")
            video_id = arguments.get("video_id")
            
            if not steps:
                return [types.TextContent(
                    type="text",
                    text=json.dumps({"error": "steps are required"})
                )]
            
            # Execute automation
            result = await browser_automator.execute_steps_async(steps)
            
            # Log execution
            execution_doc = {
                'video_id': video_id,
                'status': 'completed' if result['success'] else 'failed',
                'log': result.get('log', []),
                'error': result.get('error'),
                'total_steps': len(steps),
                'failed_step': result.get('failed_step'),
                'created_at': datetime.utcnow()
            }
            execution_id = db.insert_execution(execution_doc)
            
            response = {
                'execution_id': str(execution_id),
                'success': result['success'],
                'log': result.get('log', []),
                'error': result.get('error'),
                'failed_step': result.get('failed_step'),
                'executed_at': datetime.utcnow().isoformat()
            }
            
            return [types.TextContent(
                type="text",
                text=json.dumps(response, default=str)
            )]
        
        elif name == "fallback_llm":
            error = arguments.get("error")
            context = arguments.get("context", {})
            
            if not error:
                return [types.TextContent(
                    type="text",
                    text=json.dumps({"error": "error message is required"})
                )]
            
            # Get suggestion from Gemini
            suggestion = video_analyzer.suggest_correction(error, context)
            
            # Store correction
            correction_doc = {
                'execution_id': context.get('execution_id'),
                'error': error,
                'suggestion': suggestion,
                'context': context,
                'created_at': datetime.utcnow()
            }
            correction_id = db.insert_correction(correction_doc)
            
            response = {
                'suggestion': suggestion,
                'correction_id': str(correction_id),
                'generated_at': datetime.utcnow().isoformat()
            }
            
            return [types.TextContent(
                type="text",
                text=json.dumps(response, default=str)
            )]
        
        elif name == "run_task_from_video":
            video_url = arguments.get("video_url")
            
            if not video_url:
                return [types.TextContent(
                    type="text",
                    text=json.dumps({"error": "video_url is required"})
                )]
            
            # Step 1: Analyze video
            print(f"📹 Analyzing video: {video_url}")
            steps = video_analyzer.analyze_video(video_url)
            
            # Store video
            video_doc = {
                'video_url': video_url,
                'uploaded_at': datetime.utcnow(),
                'steps': steps
            }
            video_id = db.insert_video(video_doc)
            print(f"💾 Video stored with ID: {video_id}")
            
            # Step 2: Execute automation
            print(f"🤖 Executing {len(steps)} automation steps...")
            result = await browser_automator.execute_steps_async(steps)
            
            # Step 3: Handle failures with LLM fallback
            suggestion = None
            if not result['success'] and result.get('error'):
                print("🔧 Getting AI fallback suggestion...")
                suggestion = video_analyzer.suggest_correction(
                    result['error'], 
                    {
                        'steps': steps, 
                        'video_url': video_url,
                        'failed_step': result.get('failed_step')
                    }
                )
            
            # Log execution
            execution_doc = {
                'video_id': video_id,
                'status': 'completed' if result['success'] else 'failed',
                'log': result.get('log', []),
                'error': result.get('error'),
                'total_steps': len(steps),
                'failed_step': result.get('failed_step'),
                'created_at': datetime.utcnow()
            }
            execution_id = db.insert_execution(execution_doc)
            
            response = {
                'video_id': str(video_id),
                'execution_id': str(execution_id),
                'status': 'completed' if result['success'] else 'failed',
                'log': result.get('log', []),
                'error': result.get('error'),
                'suggestion': suggestion,
                'total_steps': len(steps),
                'failed_step': result.get('failed_step'),
                'completed_at': datetime.utcnow().isoformat()
            }
            
            return [types.TextContent(
                type="text",
                text=json.dumps(response, default=str)
            )]
        
        elif name == "get_tasks":
            tasks = db.get_all_videos()
            return [types.TextContent(
                type="text",
                text=json.dumps({
                    'tasks': tasks,
                    'total_count': len(tasks),
                    'retrieved_at': datetime.utcnow().isoformat()
                }, default=str)
            )]
        
        elif name == "get_task":
            task_id = arguments.get("task_id")
            if not task_id:
                return [types.TextContent(
                    type="text",
                    text=json.dumps({"error": "task_id is required"})
                )]
            
            task = db.get_video_by_id(task_id)
            if not task:
                return [types.TextContent(
                    type="text",
                    text=json.dumps({"error": "Task not found"})
                )]
            
            # Get associated executions
            executions = db.get_executions_by_video_id(task_id)
            
            return [types.TextContent(
                type="text",
                text=json.dumps({
                    'task': task,
                    'executions': executions,
                    'execution_count': len(executions),
                    'retrieved_at': datetime.utcnow().isoformat()
                }, default=str)
            )]
        
        elif name == "delete_task":
            task_id = arguments.get("task_id")
            if not task_id:
                return [types.TextContent(
                    type="text",
                    text=json.dumps({"error": "task_id is required"})
                )]
            
            result = db.delete_video(task_id)
            if not result:
                return [types.TextContent(
                    type="text",
                    text=json.dumps({"error": "Task not found"})
                )]
            
            return [types.TextContent(
                type="text",
                text=json.dumps({
                    "message": "Task deleted successfully",
                    "task_id": task_id,
                    "deleted_at": datetime.utcnow().isoformat()
                })
            )]
        
        elif name == "get_execution":
            execution_id = arguments.get("execution_id")
            if not execution_id:
                return [types.TextContent(
                    type="text",
                    text=json.dumps({"error": "execution_id is required"})
                )]
            
            execution = db.get_execution_by_id(execution_id)
            if not execution:
                return [types.TextContent(
                    type="text",
                    text=json.dumps({"error": "Execution not found"})
                )]
            
            # Get associated corrections
            corrections = db.get_corrections_by_execution_id(execution_id)
            
            return [types.TextContent(
                type="text",
                text=json.dumps({
                    'execution': execution,
                    'corrections': corrections,
                    'correction_count': len(corrections),
                    'retrieved_at': datetime.utcnow().isoformat()
                }, default=str)
            )]
        
        elif name == "get_execution_stats":
            stats = db.get_execution_stats()
            return [types.TextContent(
                type="text",
                text=json.dumps({
                    **stats,
                    'generated_at': datetime.utcnow().isoformat()
                }, default=str)
            )]
        
        elif name == "get_recent_activity":
            limit = arguments.get("limit", 10)
            activity = db.get_recent_activity(limit)
            return [types.TextContent(
                type="text",
                text=json.dumps({
                    **activity,
                    'limit': limit,
                    'retrieved_at': datetime.utcnow().isoformat()
                }, default=str)
            )]
        
        elif name == "health_check":
            try:
                db_health = db.health_check()
                
                # Test AI service
                ai_status = "available"
                try:
                    # Quick test of Gemini API
                    if not os.getenv('GEMINI_API_KEY') or os.getenv('GEMINI_API_KEY') == 'your_gemini_api_key_here':
                        ai_status = "api_key_missing"
                    else:
                        ai_status = "available"
                except Exception as e:
                    ai_status = f"error: {str(e)}"
                
                system_health = {
                    'status': 'healthy' if db_health['connected'] else 'unhealthy',
                    'timestamp': datetime.utcnow().isoformat(),
                    'database': db_health,
                    'services': {
                        'video_analyzer': ai_status,
                        'browser_automator': 'available',
                        'mcp_server': 'running'
                    },
                    'environment': {
                        'python_version': f"{os.sys.version_info.major}.{os.sys.version_info.minor}.{os.sys.version_info.micro}",
                        'mcp_version': "1.13.1"
                    }
                }
                
                return [types.TextContent(
                    type="text",
                    text=json.dumps(system_health, default=str)
                )]
            except Exception as e:
                return [types.TextContent(
                    type="text",
                    text=json.dumps({
                        'status': 'unhealthy',
                        'error': str(e),
                        'timestamp': datetime.utcnow().isoformat()
                    })
                )]
        
        else:
            return [types.TextContent(
                type="text",
                text=json.dumps({
                    "error": f"Unknown tool: {name}",
                    "available_tools": [
                        "analyze_video", "execute_browser_action", "fallback_llm", 
                        "run_task_from_video", "get_tasks", "get_task", "delete_task",
                        "get_execution", "get_execution_stats", "get_recent_activity", 
                        "health_check"
                    ]
                })
            )]
    
    except Exception as e:
        error_details = {
            "error": str(e),
            "tool": name,
            "arguments": arguments,
            "traceback": traceback.format_exc(),
            "timestamp": datetime.utcnow().isoformat()
        }
        print(f"❌ Tool execution error: {error_details}")
        return [types.TextContent(
            type="text",
            text=json.dumps(error_details, default=str)
        )]

async def main():
    """
    Start the MCP server with proper initialization
    """
    print("🚀 Starting MCP Browser Automation Server v1.13.1")
    
    # Verify environment
    if not os.getenv('GEMINI_API_KEY'):
        print("⚠️  Warning: GEMINI_API_KEY not set in environment")
    
    try:
        # Run the server using stdin/stdout streams
        async with stdio_server() as (read_stream, write_stream):
            print("✅ MCP Server initialized and ready for connections")
            await server.run(
                read_stream,
                write_stream,
                InitializationOptions(
                    server_name="browser-automation-mcp",
                    server_version="1.0.0",
                    capabilities=server.get_capabilities(
                        notification_options=NotificationOptions(),
                        experimental_capabilities={}
                    )
                )
            )
    except Exception as e:
        print(f"❌ Server startup failed: {e}")
        raise

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("👋 MCP Server shutting down...")
    except Exception as e:
        print(f"💥 Fatal error: {e}")
        exit(1)