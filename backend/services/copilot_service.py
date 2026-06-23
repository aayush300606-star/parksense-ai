import os
import json
from datetime import datetime
from typing import List, Dict, Any

from ..models.scac_intelligence import SmartCityKnowledgeObject
from ..ai.copilot_orchestrator import CopilotOrchestrator
from ..ai.specialized_advisors import (
    ExecutiveInsightEngine,
    DashboardSummaryEngine,
    EnforcementAdvisor,
    PredictionAdvisor,
    SimulationAdvisor
)

class CopilotService:
    """
    Service wrapper for SCAC APIs.
    """

    @staticmethod
    def query(text: str) -> Dict[str, Any]:
        result = CopilotOrchestrator.process_query(text)
        
        obj = SmartCityKnowledgeObject(
            query=result['query'],
            intent=result['intent'],
            context_sources=result['context_sources'],
            evidence=result['evidence'],
            response=result['response'],
            recommendations=result['recommendations'],
            confidence=result['confidence'],
            generated_at=datetime.now()
        )
        return obj.dict()

    @staticmethod
    def get_daily_brief():
        res = ExecutiveInsightEngine.generate_daily_brief()
        res['generated_at'] = datetime.now()
        return res
        
    @staticmethod
    def get_top_insights():
        res = DashboardSummaryEngine.get_top_insights()
        res['generated_at'] = datetime.now()
        return res

    @staticmethod
    def get_recommendations():
        res = EnforcementAdvisor.advise()
        res['generated_at'] = datetime.now()
        return res
