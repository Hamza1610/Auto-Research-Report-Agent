# auto-research-agent/agents/analysis_agent.py

import os
import google.generativeai as genai
import json
from config import GEMINI_API_KEY, GEMINI_MODEL

class AnalysisAgent:
    """
    Agent responsible for analyzing content using the Gemini API.
    """
    def __init__(self):
        if not GEMINI_API_KEY:
            raise ValueError("Gemini API key is required.")
        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel(GEMINI_MODEL)
        self.prompt_template = self._load_prompt_template()

    def _load_prompt_template(self) -> str:
        """Loads the prompt template from a file."""
        # Get the absolute path to the project root (where main.py is located)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_dir)  # Go up one level from agents/
        
        # Build absolute path for prompt template
        prompt_path = os.path.join(project_root, "prompts", "report_prompt.txt")
        
        print(f"AnalysisAgent: Loading prompt template from: {prompt_path}")
        
        with open(prompt_path, 'r') as f:
            return f.read()

    def run(self, raw_content: str) -> dict:
        """
        Analyzes the raw content with Gemini and returns structured JSON.

        Args:
            raw_content: The consolidated text from the ResearchAgent.

        Returns:
            A dictionary containing the structured insights from Gemini.
        """
        print("AnalysisAgent: Analyzing content with Gemini...")
        if not raw_content:
            print("AnalysisAgent: No content to analyze.")
            return {}

        prompt = self.prompt_template.replace("{{raw_content}}", raw_content)

        try:
            response = self.model.generate_content(prompt)
            # Clean up the response to ensure it's valid JSON
            cleaned_response = response.text.strip().replace("```json", "").replace("```", "")
            insights = json.loads(cleaned_response)
            
            print("AnalysisAgent: Successfully parsed Gemini response.")
            print(f"AnalysisAgent: Response keys: {list(insights.keys())}")
            print(f"AnalysisAgent: Title: {insights.get('title', 'No title')}")
            print(f"AnalysisAgent: Has executive_summary: {'executive_summary' in insights}")
            print(f"AnalysisAgent: Has key_insights: {'key_insights' in insights}")
            print(f"AnalysisAgent: Has source_analysis: {'source_analysis' in insights}")
            print(f"AnalysisAgent: Has conclusion: {'conclusion' in insights}")
            
            return insights
        except Exception as e:
            print(f"AnalysisAgent: Error generating or parsing Gemini response: {e}")
            print(f"AnalysisAgent: Raw response: {response.text if 'response' in locals() else 'No response'}")
            # Fallback or error handling
            return {"error": "Failed to generate analysis", "details": str(e)}