import requests
import os
from typing import Dict, Any, Optional
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class MCPClient:
    """Client to communicate with MCP server for video analysis and automation"""
    
    def __init__(self):
        self.mcp_base_url = os.getenv('MCP_SERVER_URL', 'http://localhost:8080')
        self.timeout = 30
    
    def analyze_video(self, video_path: str) -> Dict[str, Any]:
        """
        Send video to MCP server for analysis
        """
        try:
            # Convert relative path to absolute path
            abs_video_path = os.path.abspath(video_path)
            
            payload = {
                'video_url': abs_video_path  # MCP server expects video_url but handles local files
            }
            
            response = requests.post(
                f"{self.mcp_base_url}/analyze_video",
                json=payload,
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                return {
                    'success': True,
                    'data': response.json()
                }
            else:
                return {
                    'success': False,
                    'error': f"MCP server error: {response.status_code} - {response.text}"
                }
                
        except requests.exceptions.RequestException as e:
            return {
                'success': False,
                'error': f"Failed to connect to MCP server: {str(e)}"
            }
        except Exception as e:
            return {
                'success': False,
                'error': f"Unexpected error: {str(e)}"
            }
    
    def execute_automation(self, steps: list, video_id: str) -> Dict[str, Any]:
        """
        Execute browser automation steps via MCP server
        """
        try:
            payload = {
                'steps': steps,
                'video_id': video_id
            }
            
            response = requests.post(
                f"{self.mcp_base_url}/execute_browser_action",
                json=payload,
                timeout=180  # Much longer timeout for automation (3 minutes)
            )
            
            if response.status_code == 200:
                return {
                    'success': True,
                    'data': response.json()
                }
            else:
                return {
                    'success': False,
                    'error': f"Automation failed: {response.status_code} - {response.text}"
                }
                
        except requests.exceptions.RequestException as e:
            return {
                'success': False,
                'error': f"Failed to connect to MCP server: {str(e)}"
            }
        except Exception as e:
            return {
                'success': False,
                'error': f"Unexpected error: {str(e)}"
            }
    
    def run_complete_workflow(self, video_path: str) -> Dict[str, Any]:
        """
        Run complete workflow: analyze + execute automation
        """
        try:
            abs_video_path = os.path.abspath(video_path)
            
            payload = {
                'video_url': abs_video_path
            }
            
            response = requests.post(
                f"{self.mcp_base_url}/run_task_from_video",
                json=payload,
                timeout=300  # Extended timeout for complete workflow (5 minutes)
            )
            
            if response.status_code == 200:
                return {
                    'success': True,
                    'data': response.json()
                }
            else:
                return {
                    'success': False,
                    'error': f"Workflow failed: {response.status_code} - {response.text}"
                }
                
        except requests.exceptions.RequestException as e:
            return {
                'success': False,
                'error': f"Failed to connect to MCP server: {str(e)}"
            }
        except Exception as e:
            return {
                'success': False,
                'error': f"Unexpected error: {str(e)}"
            }
    
    def health_check(self) -> bool:
        """
        Check if MCP server is running
        """
        try:
            response = requests.get(f"{self.mcp_base_url}/health", timeout=5)
            return response.status_code == 200
        except:
            return False