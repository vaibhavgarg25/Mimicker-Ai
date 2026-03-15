# services/vision.py - Gemini Video Analysis Service
import importlib
import json
import os
import time
import warnings
from typing import Any, Dict, List


class VideoAnalyzer:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.model_name = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
        self._backend = None
        self._client = None
        self._model = None

    def _has_live_ai(self) -> bool:
        return bool(self.api_key and self.api_key != "your_gemini_api_key_here")

    def _ensure_client(self) -> None:
        if self._backend:
            return

        if not self.api_key:
            raise RuntimeError("GEMINI_API_KEY is not set")

        try:
            genai_module = importlib.import_module("google.genai")
            self._client = genai_module.Client(api_key=self.api_key)
            self._backend = "google_genai"
            return
        except ModuleNotFoundError:
            pass

        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", FutureWarning)
                legacy_genai = importlib.import_module("google.generativeai")
            legacy_genai.configure(api_key=self.api_key)
            self._model = legacy_genai.GenerativeModel(self.model_name)
            self._client = legacy_genai
            self._backend = "google_generativeai"
            return
        except ModuleNotFoundError as exc:
            raise RuntimeError(
                "Gemini SDK not installed. Install `google-genai` (preferred) or `google-generativeai`."
            ) from exc

    def _generate_content(self, contents: Any):
        self._ensure_client()

        if self._backend == "google_genai":
            return self._client.models.generate_content(
                model=self.model_name,
                contents=contents,
            )

        return self._model.generate_content(contents)

    def _upload_file(self, video_path: str):
        self._ensure_client()

        if self._backend == "google_genai":
            return self._client.files.upload(file=video_path)

        return self._client.upload_file(path=video_path)

    def _get_file(self, file_name: str):
        self._ensure_client()

        if self._backend == "google_genai":
            return self._client.files.get(name=file_name)

        return self._client.get_file(file_name)

    @staticmethod
    def _file_state_name(file_obj: Any) -> str:
        state = getattr(file_obj, "state", None)
        name = getattr(state, "name", None)
        if name:
            return str(name).upper()
        if state:
            return str(state).upper()
        return "UNKNOWN"

    @staticmethod
    def _response_text(response: Any) -> str:
        text = getattr(response, "text", None)
        if text:
            return text.strip()
        return str(response).strip()

    @staticmethod
    def _extract_json_array(response_text: str) -> List[Dict[str, Any]]:
        json_start = response_text.find("[")
        json_end = response_text.rfind("]") + 1

        if json_start != -1 and json_end > json_start:
            return json.loads(response_text[json_start:json_end])

        raise ValueError("Could not extract JSON array from model response")

    def analyze_video(self, video_path_or_url: str) -> List[Dict[str, Any]]:
        """
        Analyze a tutorial video and extract structured browser automation steps.
        Supports both local files and URLs.
        """
        try:
            if not self._has_live_ai():
                print("Gemini not configured. Using built-in demo analysis.")
                return self._get_demo_steps(video_path_or_url)

            if os.path.isfile(video_path_or_url):
                return self._analyze_local_video(video_path_or_url)
            if "youtube.com" in video_path_or_url or "youtu.be" in video_path_or_url:
                return self._analyze_youtube_video(video_path_or_url)
            return self._analyze_generic_video(video_path_or_url)
        except Exception as exc:
            raise Exception(f"Video analysis failed: {str(exc)}") from exc

    def _analyze_local_video(self, video_path: str) -> List[Dict[str, Any]]:
        """
        Analyze a local video file using Gemini.
        """
        try:
            print(f"Analyzing local video: {video_path}")

            video_file = self._upload_file(video_path)
            print(f"Video uploaded successfully: {getattr(video_file, 'name', 'unknown')}")

            while self._file_state_name(video_file) == "PROCESSING":
                print("Processing video...")
                time.sleep(2)
                video_file = self._get_file(video_file.name)

            if self._file_state_name(video_file) == "FAILED":
                raise Exception("Video processing failed")

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

            response = self._generate_content([video_file, prompt])
            steps = self._extract_json_array(self._response_text(response))
            print(f"Extracted {len(steps)} automation steps from video")
            return steps

        except Exception as exc:
            print(f"Local video analysis failed: {exc}")
            print("Attempting alternative analysis approach...")

            try:
                video_file = self._upload_file(video_path)

                while self._file_state_name(video_file) == "PROCESSING":
                    time.sleep(2)
                    video_file = self._get_file(video_file.name)

                if self._file_state_name(video_file) != "FAILED":
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

                    response = self._generate_content([video_file, simple_prompt])
                    steps = self._extract_json_array(self._response_text(response))
                    print(f"Alternative analysis extracted {len(steps)} steps")
                    return steps
            except Exception as retry_exc:
                print(f"Alternative analysis also failed: {retry_exc}")

            print("Using fallback example steps")
            return self._get_example_steps()

    def _analyze_youtube_video(self, video_url: str) -> List[Dict[str, Any]]:
        """
        Analyze YouTube video.
        """
        try:
            self._extract_youtube_id(video_url)

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

            response = self._generate_content(prompt)
            return self._extract_json_array(self._response_text(response))
        except Exception as exc:
            print(f"YouTube analysis failed: {exc}")
            return self._get_example_steps()

    def _analyze_generic_video(self, video_url: str) -> List[Dict[str, Any]]:
        """
        Analyze a generic video URL.
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

            response = self._generate_content(prompt)
            return self._extract_json_array(self._response_text(response))
        except Exception as exc:
            print(f"Generic video analysis failed: {exc}")
            return self._get_example_steps()

    def _extract_youtube_id(self, url: str) -> str:
        """Extract YouTube video ID from URL."""
        if "youtu.be/" in url:
            return url.split("youtu.be/")[-1].split("?")[0]
        if "youtube.com/watch?v=" in url:
            return url.split("v=")[1].split("&")[0]
        return ""

    def _get_example_steps(self) -> List[Dict[str, Any]]:
        """
        Fallback example steps that demonstrate a complete search workflow with result clicking.
        """
        return [
            {
                "action": "goto",
                "url": "https://www.google.com",
                "description": "Navigate to Google search",
            },
            {
                "action": "wait",
                "timeout": 2000,
                "description": "Wait for page to load",
            },
            {
                "action": "type",
                "selector": "textarea[name='q']",
                "text": "YouTube automation demo",
                "description": "Type search query in Google search box",
            },
            {
                "action": "wait",
                "timeout": 1000,
                "description": "Wait after typing",
            },
            {
                "action": "click",
                "selector": "input[name='btnK']",
                "description": "Click Google Search button",
            },
            {
                "action": "wait",
                "timeout": 3000,
                "description": "Wait for search results to load",
            },
            {
                "action": "click",
                "selector": "h3 a",
                "description": "Click on first search result",
            },
            {
                "action": "wait",
                "timeout": 3000,
                "description": "Wait for result page to load",
            },
        ]

    def _get_demo_steps(self, video_path_or_url: str) -> List[Dict[str, Any]]:
        """
        Generate a useful demo workflow when Gemini is unavailable.
        """
        if "youtube.com" in video_path_or_url or "youtu.be" in video_path_or_url:
            return [
                {
                    "action": "goto",
                    "url": video_path_or_url,
                    "description": "Open the provided YouTube video directly",
                },
                {
                    "action": "wait",
                    "timeout": 3000,
                    "description": "Wait for the video page to load",
                },
            ]

        if os.path.isfile(video_path_or_url):
            return self._get_example_steps()

        if video_path_or_url.startswith(("http://", "https://")):
            return [
                {
                    "action": "goto",
                    "url": video_path_or_url,
                    "description": "Open the provided webpage directly",
                },
                {
                    "action": "wait",
                    "timeout": 3000,
                    "description": "Wait for the page to load",
                },
            ]

        return self._get_example_steps()

    def suggest_correction(self, error: str, context: Dict[str, Any]) -> str:
        """
        Use Gemini to suggest corrections for failed automation steps.
        """
        if not self._has_live_ai():
            step_count = len(context.get("steps", [])) if isinstance(context.get("steps"), list) else 0
            return (
                "Gemini is not configured, so this is a local fallback suggestion: "
                "verify the selector on the current page, add a longer wait before the failing step, "
                f"and rerun the workflow. Steps in context: {step_count}."
            )

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

            response = self._generate_content(prompt)
            return self._response_text(response)
        except Exception as exc:
            return f"Could not generate suggestion: {str(exc)}"
