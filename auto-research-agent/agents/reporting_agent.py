# auto-research-agent/agents/reporting_agent.py

import os
import uuid
from config import REPORT_TEMPLATE_PATH, TEMP_DIR
from utils.pdf_generator import generate_pdf_from_template

class ReportingAgent:
    """
    Agent responsible for creating a styled PDF report from structured data.
    It uses a utility function to handle the actual PDF generation.
    """
    def __init__(self):
        # Get the absolute path to the project root (where main.py is located)
        # This ensures template paths work regardless of current working directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_dir)  # Go up one level from agents/
        
        # Build absolute paths for templates
        self.template_dir = os.path.join(project_root, "templates")
        self.template_name = "report_template.html"

    def run(self, insights_data: dict, query: str) -> str | None:
        """
        Generates a PDF report by orchestrating the pdf_generator utility.

        Args:
            insights_data: The structured JSON data from the AnalysisAgent.
            query: The original user query, used for naming the file.

        Returns:
            The local file path of the generated PDF in the temp directory, or None on failure.
        """
        print("ReportingAgent: Generating PDF report...")
        if not insights_data or "error" in insights_data:
            print("ReportingAgent: Invalid data received, skipping PDF generation.")
            return None

        # Generate a unique, safe filename
        safe_query = "".join(c for c in query if c.isalnum()).lower()
        filename = f"report_{safe_query[:20]}_{uuid.uuid4().hex[:6]}.pdf"
        output_path = os.path.join(TEMP_DIR, filename)

        print(f"ReportingAgent: Template directory: {self.template_dir}")
        print(f"ReportingAgent: Template name: {self.template_name}")
        print(f"ReportingAgent: Output path: {output_path}")

        # Call the utility function to do the heavy lifting
        success = generate_pdf_from_template(
            data=insights_data,
            template_name=self.template_name,
            template_dir=self.template_dir,
            output_path=output_path
        )

        if success:
            print(f"ReportingAgent: PDF generation orchestrated successfully.")
            return output_path
        else:
            print(f"ReportingAgent: PDF generation failed.")
            return None