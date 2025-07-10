# auto-research-agent/tests/test_research_agent.py

import unittest
from unittest.mock import patch, MagicMock
from agents.research_agent import ResearchAgent

class TestResearchAgent(unittest.TestCase):

    @patch('agents.research_agent.WebSearchClient')
    @patch('agents.research_agent.storage.Client')
    def test_run_with_web_and_gcs(self, mock_storage_client, mock_search_client):
        """
        Tests that the agent calls both web search and GCS reading methods.
        """
        # --- Arrange ---
        # Mock the search client's return value
        mock_search_instance = mock_search_client.return_value
        mock_search_instance.search.return_value = "Web search result."

        # Mock the GCS client and blob content
        mock_blob = MagicMock()
        mock_blob.download_as_text.return_value = "GCS document content."
        mock_bucket = MagicMock()
        mock_bucket.blob.return_value = mock_blob
        mock_storage_instance = mock_storage_client.return_value
        mock_storage_instance.bucket.return_value = mock_bucket

        agent = ResearchAgent()
        query = "test query"
        gcs_paths = ["gs://fake-bucket/doc.txt"]

        # --- Act ---
        result = agent.run(query, gcs_paths)

        # --- Assert ---
        # Verify that the search client was called correctly
        mock_search_instance.search.assert_called_once_with(query)

        # Verify that the GCS client was used correctly
        mock_storage_instance.bucket.assert_called_once_with('your_source_bucket_name') # Replace with actual bucket name from config
        mock_bucket.blob.assert_called_once_with('doc.txt')
        mock_blob.download_as_text.assert_called_once()

        # Check the consolidated output
        self.assertIn("Web search result.", result)
        self.assertIn("GCS document content.", result)

if __name__ == '__main__':
    unittest.main()