from fastapi import FastAPI, HTTPException
from fastapi.responses import Response
from pydantic import BaseModel
import requests
import time
from prometheus_client import Counter, Histogram, generate_latest

app = FastAPI(title="AI Monitoring Service")

# Prometheus Metrics
REQUEST_COUNT = Counter(
    "ai_requests_total",
    "Total number of AI requests"
)

ERROR_COUNT = Counter(
    "ai_errors_total",
    "Total number of AI errors"
)

REQUEST_LATENCY = Histogram(
    "ai_request_latency_seconds",
    "Latency of AI requests"
)

RESPONSE_LENGTH = Histogram(
    "ai_response_length_chars",
    "Length of AI responses in characters"
)

# Request Model
class PromptRequest(BaseModel):
    prompt: str
    model: str = "llama3"

# Ollama Configuration
OLLAMA_URL = "http://ollama-llm:11434/api/generate"

# Endpoints
@app.post("/generate")
def generate_text(request: PromptRequest):
    REQUEST_COUNT.inc()
    start_time = time.time()

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": request.model,
                "prompt": request.prompt,
                "stream": False
            },
            timeout=60
        )

        response.raise_for_status()
        data = response.json()

        output = data.get("response", "")

        RESPONSE_LENGTH.observe(len(output))
        REQUEST_LATENCY.observe(time.time() - start_time)

        return {
            "model": request.model,
            "prompt": request.prompt,
            "response": output
        }

    except Exception as e:
        ERROR_COUNT.inc()
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type="text/plain")