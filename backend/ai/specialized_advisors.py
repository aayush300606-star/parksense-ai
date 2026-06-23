from typing import Dict, Any

from .copilot_orchestrator import CopilotOrchestrator

class ExecutiveInsightEngine:
    @staticmethod
    def generate_daily_brief() -> Dict[str, Any]:
        return CopilotOrchestrator.process_query("What is the overall city-wide summary and briefing today?")

class DashboardSummaryEngine:
    @staticmethod
    def get_top_insights() -> Dict[str, Any]:
        return CopilotOrchestrator.process_query("What are the top 10 critical priority hotspots right now?")
        
class EnforcementAdvisor:
    @staticmethod
    def advise() -> Dict[str, Any]:
        return CopilotOrchestrator.process_query("Which hotspot should police target first and dispatch to?")

class PredictionAdvisor:
    @staticmethod
    def advise() -> Dict[str, Any]:
        return CopilotOrchestrator.process_query("Which locations are likely to become critical tomorrow or in the future?")

class SimulationAdvisor:
    @staticmethod
    def advise() -> Dict[str, Any]:
        return CopilotOrchestrator.process_query("What will happen if we enforce and remove parking?")
