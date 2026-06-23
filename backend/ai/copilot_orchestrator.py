from typing import Dict, Any

from .intent_engine import IntentEngine
from .tool_registry import ToolRegistry
from .context_aggregator import ContextAggregator
from .llm_engine import LLMEngine
from .fact_verification_engine import FactVerificationEngine

class CopilotOrchestrator:
    """
    Master orchestrator for RAG reasoning flow.
    """

    @staticmethod
    def process_query(query: str) -> Dict[str, Any]:
        """
        Flow: Query -> Intent -> Tools -> Context -> LLM -> Response
        """
        print(f"SCAC™ processing query: '{query}'")
        
        intent = IntentEngine.classify(query)
        print(f"  > Intent Classified: {intent}")
        
        tools = ToolRegistry.get_tools_for_intent(intent)
        print(f"  > Tools Selected: {tools}")
        
        context = ContextAggregator.build_context(tools)
        print(f"  > Context Gathered: {len(context.keys())} intelligence blocks.")
        
        response = LLMEngine.generate_response(query, intent, context)
        print(f"  > Reasoning complete. Validating facts...")
        
        verified_response = FactVerificationEngine.verify_and_filter(response)
        
        return verified_response
