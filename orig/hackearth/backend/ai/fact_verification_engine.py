from typing import Dict, Any
from .grounding_engine import GroundingEngine

class FactVerificationEngine:
    """
    The final safeguard before an AI response is delivered to the user.
    If the Grounding Engine detects a hallucination, this engine rejects it.
    """

    @staticmethod
    def verify_and_filter(generated_payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Passes the LLM output through the Fact Validator.
        """
        response_text = generated_payload.get('response', '')
        context_sources = generated_payload.get('context_sources', [])
        
        # In a real RAG setup, context is the actual injected data. We approximate it here by passing
        # the payload evidence to the grounding engine.
        context_dump = {"evidence": generated_payload.get('evidence', []), "text": response_text}
        
        is_valid, reason = GroundingEngine.validate_response(response_text, context_dump)
        
        if not is_valid:
            print(f"  [!] FACT VERIFICATION FAILED: {reason}")
            # Rewrite response safely
            generated_payload['response'] = "The requested information could not be verified against the official platform data. To prevent hallucination, the response has been blocked."
            generated_payload['confidence'] = 0.0
            generated_payload['evidence'].append(f"BLOCKED BY FACT VERIFICATION: {reason}")
            
        generated_payload['verified_by_grounding_engine'] = True
        return generated_payload
