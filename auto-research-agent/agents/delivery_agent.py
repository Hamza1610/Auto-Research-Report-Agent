# auto-research-agent/agents/delivery_agent.py

import os
from config import GCS_REPORTS_BUCKET

class DeliveryAgent:
    """
    Agent responsible for delivering the final report by uploading it to GCS.
    """
    def __init__(self):
        # Make GCS client optional to avoid authentication errors
        self.storage_client = None
        try:
            from google.cloud import storage
            self.storage_client = storage.Client()
        except Exception as e:
            print(f"Warning: Google Cloud Storage not available: {e}")
            print("GCS upload will be disabled. Reports will only be saved locally.")
        
        self.bucket_name = GCS_REPORTS_BUCKET

    def run(self, local_pdf_path: str) -> str | None:
        """
        Uploads the generated PDF to GCS.

        Args:
            local_pdf_path: The path to the PDF file in the local filesystem (e.g., /tmp/).

        Returns:
            The public GCS URL of the uploaded file, or None on failure.
        """
        if not local_pdf_path:
            print("DeliveryAgent: No local PDF path provided. Skipping delivery.")
            return None

        if not self.storage_client:
            print("DeliveryAgent: GCS client not available. Report saved locally only.")
            print(f"Local PDF path: {local_pdf_path}")
            return None

        print(f"DeliveryAgent: Uploading {local_pdf_path} to GCS bucket {self.bucket_name}...")
        try:
            bucket = self.storage_client.bucket(self.bucket_name)
            blob_name = os.path.basename(local_pdf_path)
            blob = bucket.blob(blob_name)

            blob.upload_from_filename(local_pdf_path)

            # Make the blob publicly accessible (adjust permissions as needed for production)
            blob.make_public()
            
            print(f"DeliveryAgent: Upload successful. Public URL: {blob.public_url}")
            return blob.public_url

        except Exception as e:
            print(f"DeliveryAgent: Failed to upload to GCS. Error: {e}")
            return None