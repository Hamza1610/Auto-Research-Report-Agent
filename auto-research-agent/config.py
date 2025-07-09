# auto-research-agent/config.py

import os
import tempfile
from dotenv import load_dotenv

# Load environment variables from a .env file for local development
load_dotenv()

# --- Google Cloud Configuration ---
GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID")
GCP_REGION = os.getenv("GCP_REGION", "us-central1")

# --- Google Gemini API ---
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = "gemini-2.5-flash" # Or another suitable model

# --- Web Search API (Serper) ---
SERPER_API_KEY = os.getenv("SERPER_API_KEY")

# --- Google Cloud Storage ---
# Bucket to read source documents from (if any)
GCS_SOURCE_BUCKET = os.getenv("GCS_SOURCE_BUCKET")

# Bucket to write the final PDF reports to
GCS_REPORTS_BUCKET = os.getenv("GCS_REPORTS_BUCKET")

# --- Project Constants ---
# Path to the Gemini prompt template
PROMPT_TEMPLATE_PATH = "prompts/report_prompt.txt"

# Path to the HTML template for the PDF report
REPORT_TEMPLATE_PATH = "templates/report_template.html"

# Temporary directory for file operations - cross-platform compatible
TEMP_DIR = tempfile.gettempdir()