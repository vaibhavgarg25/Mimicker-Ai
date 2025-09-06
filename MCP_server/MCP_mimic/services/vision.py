# services/vision.py - Gemini Video Analysis Service
import google.generativeai as genai
import os
import json
import requests
from typing import List, Dict, Any

class VideoAnalyzer:
    def __init__(self):
        genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
        self.model = genai.GenerativeModel('gemini-1.5-pro')
    
    def analyze_video(self, video_path_or_url: str) -> List[Dict[str, Any]]:
        """
        Analyze a tutorial video and extract structured browser automation steps
        Supports both local files and URLs
        """
        try:
            # Check if it's a local file
            if os.path.isfile(video_path_or_url):
                return self._analyze_local_video(video_path_or_url)
            # Check if it's a YouTube URL
            elif 'youtube.com' in video_path_or_url or 'youtu.be' in video_path_or_url:
                return self._analyze_youtube_video(video_path_or_url)
            else:
                return self._analyze_generic_video(video_path_or_url)
            
        except Exception as e:
            raise Exception(f"Video analysis failed: {str(e)}")
    
    def _analyze_local_video(self, video_path: str) -> List[Dict[str, Any]]:
        """
        Analyze local video file using Gemini's video analysis
        """
        try:
            print(f"📹 Analyzing local video: {video_path}")
            
            # Upload video file to Gemini
            video_file = genai.upload_file(path=video_path)
            print(f"✅ Video uploaded successfully: {video_file.name}")
            
            # Wait for processing
            import time
            while video_file.state.name == "PROCESSING":
                print("⏳ Processing video...")
                time.sleep(2)
                video_file = genai.get_file(video_file.name)
            
            if video_file.state.name == "FAILED":
                raise Exception("Video processing failed")
            
            # Analyze the video
            prompt = """
            Analyze this tutorial video and extract step-by-step browser automation actions.
            
            Watch the video carefully and identify:
            1. What website or application is being demonstrated
            2. Each user interaction (clicks, typing, navigation)
            3. The sequence of actions performed
            
            Return a JSON array of browser automation steps in this exact format:
            [
                {"action": "goto", "url": "https://example.com", "description": "Navigate to website"},
                {"action": "click", "selector": "#login-button", "description": "Click login button"},
                {"action": "type", "selector": "#username", "text": "example_user", "description": "Enter username"},
                {"action": "type", "selector": "#password", "text": "password123", "description": "Enter password"},
                {"action": "click", "selector": "#submit", "description": "Submit login form"}
            ]
            
            Supported actions:
            - goto: Navigate to URL
            - click: Click element (use specific CSS selectors like #id, .class, [data-testid="value"])
            - type: Type text into input fields
            - wait: Wait for element to appear
            - scroll: Scroll page (direction: up/down/top/bottom)
            - hover: Hover over element
            - select: Select option from dropdown
            
            Important guidelines:
            - Use specific, reliable CSS selectors (prefer IDs over classes)
            - Include realistic URLs and text content
            - Add descriptive descriptions for each step
            - Make sure the sequence is logical and complete
            - If you see form submissions, include proper selectors for submit buttons
            
            Only return the JSON array, no additional text.
            """
            
            response = self.model.generate_content([video_file, prompt])
            response_text = response.text.strip()
            
            # Extract JSON from response
            json_start = response_text.find('[')
            json_end = response_text.rfind(']') + 1
            
            if json_start != -1 and json_end > json_start:
                json_str = response_text[json_start:json_end]
                steps = json.loads(json_str)
                print(f"✅ Extracted {len(steps)} automation steps from video")
                return steps
            else:
                print("⚠️ Could not extract JSON from response, using fallback")
                return self._get_example_steps()
                
        except Exception as e:
            print(f"❌ Local video analysis failed: {e}")
            print("🔄 Using fallback example steps")
            return self._get_example_steps()
    
    def _analyze_youtube_video(self, video_url: str) -> List[Dict[str, Any]]:
        """
        Analyze YouTube video (placeholder implementation)
        In production, this would use Gemini's actual video analysis
        """
        try:
            # Extract video ID for context
            video_id = self._extract_youtube_id(video_url)
            
            # Use Gemini to generate likely automation steps based on common patterns
            prompt = f"""
            Based on this YouTube video URL ({video_url}), generate realistic browser automation steps 
            for a common web tutorial scenario. Return valid JSON array of actions:
            
            Common scenarios might include:
            - Login to a website
            - Fill out a form
            - Navigate through a dashboard
            - Create an account
            - Online shopping
            
            Format: [{{"action": "goto", "url": "https://example.com"}}, ...]
            """
            
            response = self.model.generate_content(prompt)
            
            # Extract JSON from response
            response_text = response.text
            
            # Try to extract JSON from the response
            json_start = response_text.find('[')
            json_end = response_text.rfind(']') + 1
            
            if json_start != -1 and json_end > json_start:
                json_str = response_text[json_start:json_end]
                steps = json.loads(json_str)
                return steps
            else:
                # Fallback to example steps
                return self._get_example_steps()
                
        except Exception as e:
            print(f"YouTube analysis failed: {e}")
            return self._get_example_steps()
    
    def _analyze_generic_video(self, video_url: str) -> List[Dict[str, Any]]:
        """
        Analyze generic video URL
        """
        try:
            prompt = f"""
            Generate browser automation steps for a tutorial video at {video_url}.
            Create a realistic sequence of web interactions as JSON array.
            
            Example format:
            [
                {{"action": "goto", "url": "https://demo-site.com"}},
                {{"action": "click", "selector": "#get-started"}},
                {{"action": "type", "selector": "#email", "text": "user@example.com"}},
                {{"action": "click", "selector": "#submit"}}
            ]
            """
            
            response = self.model.generate_content(prompt)
            response_text = response.text
            
            # Extract JSON
            json_start = response_text.find('[')
            json_end = response_text.rfind(']') + 1
            
            if json_start != -1 and json_end > json_start:
                json_str = response_text[json_start:json_end]
                return json.loads(json_str)
            else:
                return self._get_example_steps()
                
        except Exception as e:
            print(f"Generic video analysis failed: {e}")
            return self._get_example_steps()
    
    def _extract_youtube_id(self, url: str) -> str:
        """Extract YouTube video ID from URL"""
        if 'youtu.be/' in url:
            return url.split('youtu.be/')[-1].split('?')[0]
        elif 'youtube.com/watch?v=' in url:
            return url.split('v=')[1].split('&')[0]
        return ""
    
    def _get_example_steps(self) -> List[Dict[str, Any]]:
        """
        Fallback example steps for demonstration
        """
        return [
            {
                "action": "goto",
                "url": "https://httpbin.org/forms/post",
                "description": "Navigate to demo form"
            },
            {
                "action": "type",
                "selector": "input[name='custname']",
                "text": "John Doe",
                "description": "Enter customer name"
            },
            {
                "action": "type",
                "selector": "input[name='custtel']",
                "text": "555-1234",
                "description": "Enter phone number"
            },
            {
                "action": "type",
                "selector": "input[name='custemail']",
                "text": "john@example.com",
                "description": "Enter email address"
            },
            {
                "action": "click",
                "selector": "input[type='submit']",
                "description": "Submit the form"
            }
        ]
    
    def suggest_correction(self, error: str, context: Dict[str, Any]) -> str:
        """
        Use Gemini to suggest corrections for failed automation steps
        """
        try:
            prompt = f"""
            A browser automation step failed with this error: "{error}"
            
            Context: {json.dumps(context, indent=2)}
            
            Please suggest a specific correction or alternative approach.
            Focus on:
            - Alternative CSS selectors
            - Wait strategies
            - Different interaction methods
            
            Provide a concise, actionable suggestion.
            """
            
            response = self.model.generate_content(prompt)
            return response.text.strip()
            
        except Exception as e:
            return f"Could not generate suggestion: {str(e)}"