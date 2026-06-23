from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Dict, Any
from ..services.copilot_service import CopilotService

router = APIRouter(prefix="/api/copilot")

class QueryRequest(BaseModel):
    query: str

@router.post("/query")
def process_query(req: QueryRequest):
    """Answers a natural language query using RAG over platform intelligence."""
    return CopilotService.query(req.query)

@router.get("/daily-brief")
def get_daily_brief():
    """Generates the executive daily briefing."""
    return CopilotService.get_daily_brief()

@router.get("/top-insights")
def get_top_insights():
    """Returns narrative summaries of the most critical current issues."""
    return CopilotService.get_top_insights()

@router.get("/recommendations")
def get_recommendations():
    """Returns narrative enforcement recommendations."""
    return CopilotService.get_recommendations()
