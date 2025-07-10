# auto-research-agent/tests/test_analysis_agent.py

import unittest
import json
from unittest.mock import patch, MagicMock
from agents.analysis_agent import AnalysisAgent

class TestAnalysisAgent(unittest.TestCase):

    def setUp(self):
        """Set up a mock prompt template file content."""
        self.mock_prompt_content = "Analyze this: {{raw_content}}"
        # This mocks the `open` function when called within the AnalysisAgent's constructor
        self.mock_open = unittest.mock.mock_open(read_data=self.mock_prompt_content)

    @patch('agents.analysis_agent.genai.GenerativeModel')
    def test_run_success(self, mock_generative_model):
        """
        Tests the successful analysis of content where Gemini returns valid JSON.
        """
        # --- Arrange ---
        # Mock the API response
        mock_response = MagicMock()
        expected_dict = {
            "title": "Test Report",
            "executive_summary": "This is a test."
        }
        mock_response.text = json.dumps(expected_dict)
        
        # Configure the mock model instance to return the mock response
        mock_model_instance = mock_generative_model.return_value
        mock_model_instance.generate_content.return_value = mock_response

        # Patch `open` to avoid file I/O in the test
        with patch('builtins.open', self.mock_open):
            agent = AnalysisAgent()

        # --- Act ---
        result = agent.run("Some raw content.")

        # --- Assert ---
        mock_model_instance.generate_content.assert_called_once()
        self.assertEqual(result, expected_dict)
        self.assertNotIn("error", result)

    @patch('agents.analysis_agent.genai.GenerativeModel')
    def test_run_api_failure(self, mock_generative_model):
        """
        Tests the agent's behavior when the Gemini API call raises an exception.
        """
        # --- Arrange ---
        # Configure the mock model to raise an error
        mock_model_instance = mock_generative_model.return_value
        mock_model_instance.generate_content.side_effect = Exception("API connection failed")

        with patch('builtins.open', self.mock_open):
            agent = AnalysisAgent()

        # --- Act ---
        result = agent.run("Some raw content.")

        # --- Assert ---
        self.assertIn("error", result)
        self.assertEqual(result["error"], "Failed to generate analysis")
        self.assertIn("API connection failed", result["details"])

    @patch('agents.analysis_agent.genai.GenerativeModel')
    def test_run_malformed_json_response(self, mock_generative_model):
        """
        Tests the agent's behavior when Gemini returns a string that is not valid JSON.
        """
        # --- Arrange ---
        mock_response = MagicMock()
        # Malformed JSON (trailing comma)
        mock_response.text = '{"title": "Test Report", "summary": "A test",}'
        
        mock_model_instance = mock_generative_model.return_value
        mock_model_instance.generate_content.return_value = mock_response

        with patch('builtins.open', self.mock_open):
            agent = AnalysisAgent()

        # --- Act ---
        result = agent.run("Some raw content.")

        # --- Assert ---
        self.assertIn("error", result)
        self.assertEqual(result["error"], "Failed to generate analysis")
        self.assertIn("JSONDecodeError", result["details"]) # Check if the error detail mentions JSON decoding

if __name__ == '__main__':
    unittest.main()