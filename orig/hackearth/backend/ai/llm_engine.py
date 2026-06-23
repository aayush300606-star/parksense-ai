from typing import Dict, Any
import json

class LLMEngine:
    """
    Reasoning layer. For this hackathon prototype, we simulate the RAG generation 
    using deterministic NLP logic to ensure absolute safety and 0 hallucinations, 
    but structured exactly as an LLM chain.
    """

    @staticmethod
    def generate_response(query: str, intent: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Reasons over the context to answer the query.
        """
        response = ""
        evidence = []
        recommendations = []
        confidence = 0.95
        
        if intent == "HOTSPOT_INQUIRY":
            top_hs = context.get('top_critical_hotspots', [])
            if top_hs:
                hs = top_hs[0]
                response = f"The most critical hotspot currently is {hs['road_name']} with a CSI of {hs['csi_score']}."
                evidence.append(f"CSI Score: {hs['csi_score']}, PIS Priority: {hs.get('priority_level', 'Unknown')}")
                recommendations.append(f"Immediate targeted enforcement recommended at {hs['road_name']}.")
            else:
                response = "There are no critical hotspots detected at this time."
                
        elif intent == "ENFORCEMENT_PLAN":
            plan = context.get('daily_enforcement_plan', {})
            targets = context.get('top_enforcement_targets', [])
            if targets:
                t1 = targets[0]
                response = f"You should dispatch {t1['recommended_team']} to {t1['road_name']} between {t1['recommended_time']}."
                evidence.append(f"This is Priority #1 due to CSI {t1['priority_score']} and {t1['expected_capacity_recovery']}% expected capacity recovery.")
                recommendations.append(t1['explanation'])
            else:
                response = "The Smart Enforcement Planner has not generated any targets yet."
                
        elif intent == "PREDICTION_INQUIRY":
            preds = context.get('predicted_high_risk_tomorrow', [])
            if preds:
                p1 = preds[0]
                risk = p1['forecasts']['24h']['hotspot_probability'] * 100
                response = f"Tomorrow, {p1['road_name']} is predicted to become a severe bottleneck."
                evidence.append(f"24h Forecast Probability: {risk:.1f}%. Trend: {p1['forecasts']['24h']['trend_direction']}.")
                recommendations.append("Pre-emptively schedule patrols before the peak hour tomorrow.")
            else:
                response = "No new severe bottlenecks are predicted for tomorrow."
                
        elif intent == "SIMULATION_REQUEST":
            sims = context.get('best_simulations', [])
            if sims:
                s1 = sims[0]
                response = f"If you apply '{s1['best_scenario']}' at {s1['road_name']}, the CSI will improve by {s1['csi_improvement']} points."
                evidence.append(f"Expected ROI: {s1['roi']}. Benefit Score: {s1['benefit_score']}/100.")
                recommendations.append(f"Execute {s1['best_scenario']} at {s1['road_name']} immediately.")
            else:
                response = "Simulation data is currently unavailable."
                
        elif intent == "EXECUTIVE_SUMMARY":
            summ = context.get('city_summary', {})
            response = f"The city currently has an average CSI of {summ.get('average_csi', 0)} across 100 monitored locations."
            evidence.append(f"Top dominant factor causing congestion: {list(summ.get('dominant_factor_distribution', {}).keys())[0] if summ.get('dominant_factor_distribution') else 'Unknown'}.")
            recommendations.append("Review the full Executive Dashboard for detailed geographic heatmaps.")
            
        else:
            response = "I can help you analyze hotspots, simulate enforcement impacts, or predict future congestion. How can I assist you today?"
            
        return {
            "query": query,
            "intent": intent,
            "context_sources": list(context.keys()),
            "evidence": evidence,
            "response": response,
            "recommendations": recommendations,
            "confidence": confidence
        }
