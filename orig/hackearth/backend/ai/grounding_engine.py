import re
from typing import Dict, Any, Tuple
from .location_guard import LocationGuard

class GroundingEngine:
    """
    Validates that every claim made by the AI maps directly to retrieved data.
    Detects hallucinations in locations, metrics, and generated statistics.
    """

    @staticmethod
    def extract_locations(text: str) -> list[str]:
        """Naively extracts capitalized phrases as potential locations."""
        # Simple regex for Capitalized Words (excluding start of sentences ideally, but good enough for prototype)
        words = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', text)
        return [w for w in words if w.lower() not in ['the', 'this', 'there', 'if', 'you', 'execute', 'immediate']]

    @staticmethod
    def extract_numbers(text: str) -> list[str]:
        return re.findall(r'\b\d+(?:\.\d+)?\b', text)

    @staticmethod
    def validate_response(response_text: str, context: Dict[str, Any]) -> Tuple[bool, str]:
        """
        Returns (is_valid, reason)
        """
        
        # 1. Location Hallucination Check
        potential_locations = GroundingEngine.extract_locations(response_text)
        for loc in potential_locations:
            if not LocationGuard.is_location_valid(loc):
                return False, f"Location Hallucination Detected: '{loc}' does not exist in the city platform data."

        # 2. Metric Hallucination Check (Strict)
        # We ensure that if a number is mentioned in the response, it exists somewhere in the stringified context.
        context_str = str(context)
        mentioned_numbers = GroundingEngine.extract_numbers(response_text)
        
        for num in mentioned_numbers:
            if num not in context_str:
                # Allow small integers like 1, 2 (often used for counts/formatting) or confidence values
                if float(num) > 10.0: 
                    return False, f"Metric Hallucination Detected: Value '{num}' was generated but not found in source data."

        return True, "Passed all grounding checks."
