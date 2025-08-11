from fastapi import FastAPI, HTTPException, Security, Request, Header
from fastapi.responses import FileResponse, JSONResponse
from fastapi.security import APIKeyHeader
from pydantic import BaseModel
import aioredis
import datetime
import os

from api.routes import router
from config import REDIS_URL
from services.helix_client import HelixClient

# --- Configuration ---
API_KEY_NAME = "Authorization"
API_KEY_HEADER = APIKeyHeader(name=API_KEY_NAME, auto_error=True)

# In a real application, this would be a database of paying users.
# This key simulates a user with an active subscription.
VALID_API_KEYS = {
    os.environ.get("NEXA_API_KEY", "nexa-free-trial-key-7-days")
}

# --- Pydantic Models ---
class QueryRequest(BaseModel):
    topic: str
    model: str
    temperature: float
    credentials: dict

class Report(BaseModel):
    title: str
    summary: str
    sources: list[str]

class QueryResponse(BaseModel):
    report: Report

# --- FastAPI App ---
app = FastAPI(
    title="Nexa Research Agent API",
    description="A simple API for the Nexa Research Agent.",
    version="1.0.0",
)

@app.on_event("startup")
async def startup_event():
    app.state.redis = await aioredis.from_url(REDIS_URL)
    app.state.helix = HelixClient()

@app.on_event("shutdown")
async def shutdown_event():
    await app.state.redis.close()
    await app.state.helix.client.aclose()

# Include API routes
app.include_router(router, prefix="/api/v1")

async def get_api_key(api_key_header: str = Security(API_KEY_HEADER)):
    """
    Validates the API key from the Authorization header.
    The key should be sent as 'Bearer <key>'.
    """
    if " " not in api_key_header:
        raise HTTPException(status_code=401, detail="Invalid Authorization header format")

    token_prefix, token = api_key_header.split(" ", 1)

    if token_prefix != "Bearer":
        raise HTTPException(status_code=401, detail="Invalid token scheme. Use 'Bearer'.")

    # In a real SaaS, you would look up the key in your database,
    # check subscription status, rate limits, trial period, etc.
    if token not in VALID_API_KEYS:
        raise HTTPException(status_code=403, detail="Invalid or expired API Key")
    return token

@app.get("/", include_in_schema=False)
async def read_root():
    """Serves the main HTML page."""
    return FileResponse("index.html")

@app.get("/health")
async def health_check():
    return JSONResponse({
        "status": "healthy",
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "version": "1.0.0"
    })

@app.post("/query", response_model=QueryResponse)
async def run_query(request: QueryRequest, api_key: str = Security(get_api_key)):
    """
    Accepts a research topic and returns a structured report.
    Requires a valid API key.
    """
    # Placeholder for the actual research logic (plan -> search -> synthesize)
    print(f"Received query for '{request.topic}' using model '{request.model}'")
    print(f"Credentials received for user: {api_key[:12]}...") # Log securely

    # Simulate a successful research report
    dummy_report = Report(
        title=f"Research Report on: {request.topic}",
        summary="This is a synthesized summary based on multiple sources. The actual implementation would use Exa.ai and an LLM to generate this.",
        sources=[
            "https://example.com/source1",
            "https://example.com/source2",
            "https://example.com/source3",
        ],
    )
    return QueryResponse(report=dummy_report)
