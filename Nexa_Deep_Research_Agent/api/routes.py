import datetime
from hashlib import sha256

from fastapi import APIRouter, Request, HTTPException
from sentence_transformers import SentenceTransformer

from core.cache import get_cached_report, set_cached_report
from core.planner import plan_research
from core.research import iterative_research
from core.summarizer import compile_report
from schemas.query import QueryRequest, QueryResponse

router = APIRouter()

# Initialize embedding model once
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

@router.post("/query", response_model=QueryResponse)
async def query_endpoint(query: QueryRequest, request: Request):
    redis = request.app.state.redis
    helix = request.app.state.helix

    # Generate cache key
    key_hash = sha256(query.topic.encode()).hexdigest()
    cache_key = f"report:{query.user_id}:{key_hash}"

    # Try cache
    cached_report = await get_cached_report(redis, cache_key)
    if cached_report:
        return QueryResponse(success=True, report=cached_report, cached=True)

    # Use planning and research pipeline with provided pass_type ("full", "half", or "direct")
    research_plan = plan_research(query.topic)
    updated_plan = await iterative_research(research_plan, pass_type=query.pass_type)
    report_text = compile_report(updated_plan)
    report = {
        "topic": query.topic,
        "content": report_text,
        "created_at": datetime.datetime.utcnow().isoformat(),
        "user_id": query.user_id
    }

    # Cache report (TTL 1 hour)
    await set_cached_report(redis, cache_key, report, ttl=3600)

    # Compute embedding and upsert into Helix
    vector = embedding_model.encode(query.topic).tolist()
    try:
        await helix.upsert("reports", [{"id": cache_key, "vector": vector, "payload": report}])
    except Exception as e:
        # Log or ignore Helix failures
        pass

    return QueryResponse(success=True, report=report, cached=False)
