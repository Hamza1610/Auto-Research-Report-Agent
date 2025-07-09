# auto-research-agent/utils/api_clients.py

import requests
import json
from config import SERPER_API_KEY

class WebSearchClient:
    """A client for performing web searches using the Serper.dev API."""

    def __init__(self, api_key: str = SERPER_API_KEY):
        if not api_key:
            raise ValueError("Serper API key is required.")
        self.api_key = api_key
        self.search_url = "https://google.serper.dev/search"

    def search(self, query: str, max_results: int = 5) -> str:
        """
        Performs a web search and returns a concatenated string of snippets.

        Args:
            query: The search query.
            max_results: The maximum number of search results to process.

        Returns:
            A single string containing the titles and snippets of the search results.
        """
        payload = json.dumps({"q": query, "num": max_results})
        headers = {
            'X-API-KEY': self.api_key,
            'Content-Type': 'application/json'
        }

        try:
            response = requests.post(self.search_url, headers=headers, data=payload, timeout=10)
            response.raise_for_status()
            results = response.json()

            content = []
            for item in results.get("organic", []):
                title = item.get("title", "")
                snippet = item.get("snippet", "")
                content.append(f"Title: {title}\nSnippet: {snippet}\n---")

            return "\n".join(content)

        except requests.RequestException as e:
            print(f"Error during web search: {e}")
            return "" # Return empty string on failure