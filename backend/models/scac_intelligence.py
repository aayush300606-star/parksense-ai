from pydantic import BaseModel
from typing import Dict, Any, List
from datetime import datetime

class SmartCityKnowledgeObject(BaseModel):
    """
    Standardized SCAC Intelligence Object.
    Represents the AI Copilot's reasoning and response to a natural language query.
    """
    model_config = {"protected_namespaces": ()}

    query: str
    intent: str
    context_sources: List[str]
    
    evidence: List[str]
    response: str
    recommendations: List[str]
    
    confidence: float
    generated_at: datetime
