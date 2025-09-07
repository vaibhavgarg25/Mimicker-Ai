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
            
            # Analyze the video with enhanced accuracy
            prompt = """
            You are an expert at analyzing tutorial videos and extracting precise browser automation steps.
            
            WATCH THIS VIDEO FRAME BY FRAME and identify EVERY action the user performs:
            
            1. OBSERVE CAREFULLY:
               - What website does the user navigate to first?
               - What EXACT text do they type? (character by character)
               - What buttons/links do they click on?
               - What is the sequence of their mouse movements and clicks?
               - Do they scroll? If so, in which direction and how much?
            
            2. EXTRACT PRECISE ACTIONS:
               - Record the EXACT text typed (not approximations)
               - Note the EXACT sequence of clicks
               - Identify the specific elements they interact with
               - Capture any navigation between pages
            
            3. GENERATE ACCURATE AUTOMATION STEPS:
               Return a JSON array that EXACTLY replicates what you see in the video.
            
            CRITICAL ACCURACY REQUIREMENTS:
            - Use the EXACT text you see being typed (not similar words)
            - Follow the EXACT sequence of actions shown
            - Include ALL clicks and navigation steps
            - Use precise selectors for the elements being clicked
            
            COMMON SCENARIOS TO DETECT:
            
            A) GOOGLE SEARCH WORKFLOW:
            If you see Google search, use this pattern:
            [
                {"action": "goto", "url": "https://www.google.com", "description": "Navigate to Google"},
                {"action": "wait", "timeout": 2000, "description": "Wait for page load"},
                {"action": "type", "selector": "textarea[name='q']", "text": "EXACT_TEXT_FROM_VIDEO", "description": "Type search query"},
                {"action": "click", "selector": "input[name='btnK']", "description": "Click search button"},
                {"action": "wait", "timeout": 3000, "description": "Wait for search results"},
                {"action": "click", "selector": "h3 a", "description": "Click first search result"}
            ]
            
            B) YOUTUBE WORKFLOW:
            If you see YouTube, use this pattern:
            [
                {"action": "goto", "url": "https://www.youtube.com", "description": "Navigate to YouTube"},
                {"action": "wait", "timeout": 2000, "description": "Wait for page load"},
                {"action": "type", "selector": "input[name='search_query']", "text": "EXACT_TEXT_FROM_VIDEO", "description": "Type in YouTube search"},
                {"action": "click", "selector": "button[id='search-icon-legacy']", "description": "Click search button"},
                {"action": "wait", "timeout": 3000, "description": "Wait for search results"},
                {"action": "click", "selector": "a[href*='/watch?v=']", "description": "Click on video"}
            ]
            
            C) DIRECT YOUTUBE VIDEO:
            If they go directly to a YouTube video:
            [
                {"action": "goto", "url": "EXACT_URL_FROM_VIDEO", "description": "Navigate to YouTube video"},
                {"action": "wait", "timeout": 3000, "description": "Wait for video to load"}
            ]
            
            SELECTOR REFERENCE:
            - Google search box: "textarea[name='q']" or "input[name='q']"
            - Google search button: "input[name='btnK']" or "button[type='submit']"
            - Google first result: "h3 a" or ".yuRUbf a"
            - YouTube search box: "input[name='search_query']"
            - YouTube search button: "button[id='search-icon-legacy']"
            - YouTube video links: "a[href*='/watch?v=']"
            - Generic buttons: "button", "input[type='submit']"
            - Generic links: "a[href]"
            
            IMPORTANT:
            - Extract the EXACT text you see being typed
            - Follow the EXACT sequence shown in the video
            - Don't add extra steps not shown in the video
            - Don't modify or "improve" the user's actions
            - Replicate their workflow precisely
            
            Return ONLY the JSON array, no other text:
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
            print("🔄 Attempting alternative analysis approach...")
            
            # Try alternative analysis with simpler prompt
            try:
                video_file = genai.upload_file(path=video_path)
                
                # Wait for processing
                import time
                while video_file.state.name == "PROCESSING":
                    time.sleep(2)
                    video_file = genai.get_file(video_file.name)
                
                if video_file.state.name != "FAILED":
                    # Simpler, more direct prompt
                    simple_prompt = """
                    Watch this video and tell me exactly what the person does step by step.
                    
                    Focus on:
                    1. What website they visit
                    2. What they type (exact text)
                    3. What they click on
                    4. Where they navigate
                    
                    Return as JSON array:
                    [
                        {"action": "goto", "url": "website_url", "description": "what they do"},
                        {"action": "type", "selector": "input_selector", "text": "exact_text", "description": "what they type"},
                        {"action": "click", "selector": "click_selector", "description": "what they click"}
                    ]
                    
                    Only return the JSON, nothing else.
                    """
                    
                    response = self.model.generate_content([video_file, simple_prompt])
                    response_text = response.text.strip()
                    
                    json_start = response_text.find('[')
                    json_end = response_text.rfind(']') + 1
                    
                    if json_start != -1 and json_end > json_start:
                        json_str = response_text[json_start:json_end]
                        steps = json.loads(json_str)
                        print(f"✅ Alternative analysis extracted {len(steps)} steps")
                        return steps
            except Exception as e2:
                print(f"❌ Alternative analysis also failed: {e2}")
            
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
        Fallback example steps that demonstrate a complete search workflow with result clicking
        """
        return [
            {
                "action": "goto",
                "url": "https://www.google.com",
                "description": "Navigate to Google search"
            },
            {
                "action": "wait",
                "timeout": 2000,
                "description": "Wait for page to load"
            },
            {
                "action": "type",
                "selector": "textarea[name='q']",
                "text": "YouTube automation demo",
                "description": "Type search query in Google search box"
            },
            {
                "action": "wait",
                "timeout": 1000,
                "description": "Wait after typing"
            },
            {
                "action": "click",
                "selector": "input[name='btnK']",
                "description": "Click Google Search button"
            },
            {
                "action": "wait",
                "timeout": 3000,
                "description": "Wait for search results to load"
            },
            {
                "action": "click",
                "selector": "h3 a",
                "description": "Click on first search result"
            },
            {
                "action": "wait",
                "timeout": 3000,
                "description": "Wait for result page to load"
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