# auto-research-agent/agents/research_agent.py

from utils.api_clients import WebSearchClient
from config import GCS_SOURCE_BUCKET

class ResearchAgent:
    """
    Agent responsible for gathering information from web searches and GCS documents.
    """
    def __init__(self):
        self.search_client = WebSearchClient()
        # Make GCS client optional to avoid authentication errors
        self.storage_client = None
        try:
            from google.cloud import storage
            self.storage_client = storage.Client()
        except Exception as e:
            print(f"Warning: Google Cloud Storage not available: {e}")
            print("GCS document reading will be disabled. Only web search will work.")

    def _search_web(self, query: str) -> str:
        """Performs a web search for the given query."""
        print(f"ResearchAgent: Searching web for '{query}'...")
        return self.search_client.search(query)

    def _read_gcs_documents(self, gcs_paths: list[str]) -> str:
        """Reads content from a list of GCS document paths."""
        if not gcs_paths:
            return ""
        
        if not self.storage_client:
            print("ResearchAgent: GCS client not available. Skipping GCS document reading.")
            return ""

        print(f"ResearchAgent: Reading GCS documents: {gcs_paths}...")
        all_content = []
        for path in gcs_paths:
            try:
                # Expects path in the format 'gs://bucket_name/file_name.txt'
                # We only need the file name as the bucket is configured.
                blob_name = path.replace(f"gs://{GCS_SOURCE_BUCKET}/", "")
                bucket = self.storage_client.bucket(GCS_SOURCE_BUCKET)
                blob = bucket.blob(blob_name)
                content = blob.download_as_text()
                all_content.append(f"Source Document: {blob_name}\n{content}\n---")
            except Exception as e:
                print(f"Error reading GCS file {path}: {e}")
        return "\n".join(all_content)

    def run(self, query: str, gcs_paths: list[str] | None = None) -> str:
        """
        Executes the research tasks and consolidates the content.

        Args:
            query: The user's research query.
            gcs_paths: A list of GCS URIs for source documents.

        Returns:
            A single string containing all gathered information.
        """
        print("ResearchAgent: Starting research...")
        web_content = self._search_web(query)
        doc_content = self._read_gcs_documents(gcs_paths or [])

        consolidated_content = f"Web Search Results for query '{query}':\n{web_content}\n\n"
        if doc_content:
            consolidated_content += f"Internal Document Content:\n{doc_content}"

        print(f"ResearchAgent: Completed. Total content length: {len(consolidated_content)} chars.")
        return consolidated_content