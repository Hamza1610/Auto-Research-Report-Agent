# auto-research-agent/orchestrator/main_orchestrator.py

from agents.research_agent import ResearchAgent
from agents.analysis_agent import AnalysisAgent
from agents.reporting_agent import ReportingAgent
from agents.delivery_agent import DeliveryAgent

class MainOrchestrator:
    """
    Orchestrates the entire research-to-report workflow by coordinating agents.
    """
    def __init__(self):
        self.research_agent = ResearchAgent()
        self.analysis_agent = AnalysisAgent()
        self.reporting_agent = ReportingAgent()
        self.delivery_agent = DeliveryAgent()
        self.state = {}

    def _reset_state(self):
        """Resets the internal state for a new run."""
        self.state = {
            "query": None,
            "gcs_paths": None,
            "raw_content": None,
            "insights": None,
            "local_report_path": None,
            "final_report_url": None,
        }

    def run(self, query: str, gcs_paths: list[str] | None = None) -> dict:
        """
        Executes the full agentic workflow from research to delivery.

        Args:
            query: The user's research query.
            gcs_paths: Optional list of GCS document paths.

        Returns:
            A dictionary containing the final report URL and status.
        """
        self._reset_state()
        self.state["query"] = query
        self.state["gcs_paths"] = gcs_paths
        print(f"Orchestrator: Starting workflow for query: '{query}'")

        # 1. Research Step
        self.state["raw_content"] = self.research_agent.run(query, gcs_paths)
        if not self.state["raw_content"]:
            return {"status": "error", "message": "Research phase failed to gather content."}

        # 2. Analysis Step
        self.state["insights"] = self.analysis_agent.run(self.state["raw_content"])
        if not self.state["insights"] or "error" in self.state["insights"]:
            return {"status": "error", "message": "Analysis phase failed to generate insights."}

        # 3. Reporting Step
        self.state["local_report_path"] = self.reporting_agent.run(self.state["insights"], query)
        if not self.state["local_report_path"]:
            return {"status": "error", "message": "Reporting phase failed to create PDF."}

        # 4. Delivery Step (Optional - GCS upload)
        self.state["final_report_url"] = self.delivery_agent.run(self.state["local_report_path"])
        
        # Return success even if GCS upload fails, as long as local PDF was created
        print("Orchestrator: Workflow completed successfully.")
        result = {
            "status": "success",
            "local_pdf_path": self.state["local_report_path"],
            "insights": self.state["insights"]
        }
        
        if self.state["final_report_url"]:
            result["report_url"] = self.state["final_report_url"]
        else:
            result["message"] = "Report generated successfully but GCS upload failed. Check local PDF path."
        
        return result