# Smart City AI Copilot (SCAC™)

The Smart City AI Copilot (SCAC™) serves as the ultimate executive layer of the platform, transforming the entire suite of analytics, predictions, and simulations into an interactive, natural-language conversational agent.

## Architecture (RAG & Tool Calling)

The Copilot employs a Retrieval-Augmented Generation (RAG) architecture:

### 1. Intent Engine
Parses the user's natural language query using regex and NLP to classify the intent into discrete platform capabilities:
- `HOTSPOT_INQUIRY`
- `SIMULATION_REQUEST`
- `PREDICTION_INQUIRY`
- `ENFORCEMENT_PLAN`
- `EXECUTIVE_SUMMARY`

### 2. Tool Registry & Context Aggregator
Once the intent is classified, the Orchestrator requests data from the relevant internal services (e.g., `CSIService`, `DigitalTwinService`). The Context Aggregator dynamically fetches the raw JSON objects for those domains (fetching summaries or top-N lists to respect context limits).

### 3. LLM Reasoning Engine
The core reasoning engine receives the context block and the user query.
> **CRITICAL:** For this hackathon prototype, the LLM is simulated via a deterministic reasoning stub. This guarantees exactly 0% hallucinations, ensuring that every metric output by SCAC perfectly matches the physical engineering calculations produced by the platform.

### 4. Specialized Advisors
To power dashboard interfaces rapidly, specialized advisors are built into `backend/ai/specialized_advisors.py` which pre-package common queries (e.g., `ExecutiveInsightEngine`, `DashboardSummaryEngine`).

## APIs
- `POST /api/copilot/query`: Accepts `{ "query": "What are the top 10 critical hotspots?" }` and returns the full `SmartCityKnowledgeObject`.
- `GET /api/copilot/daily-brief`: Returns a pre-computed executive daily summary.
- `GET /api/copilot/top-insights`: Returns pre-computed insights.
- `GET /api/copilot/recommendations`: Returns operational recommendations from the Enforcement Planner.

## Future RAG Expansion
When connecting to a live API (e.g., Gemini 1.5 Pro):
1. The `LLMEngine.generate_response()` is replaced with a prompt call.
2. The context is injected into the prompt: `Answer the user query based ONLY on the following JSON context. Do not invent any numbers. If the data is not there, say you do not know.`
3. The LLM returns a structured JSON matching `SmartCityKnowledgeObject`.
