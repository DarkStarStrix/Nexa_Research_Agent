from fastapi import APIRouter, Request, HTTPException
import datetime
from hashlib import sha256
from schemas.query import QueryRequest, QueryResponse
from core.cache import get_cached_report, set_cached_report
from services.helix_client import HelixClient
from sentence_transformers import SentenceTransformer

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

    # Generate dummy report content (replace with real pipeline)
    report = {
        "topic": query.topic,
        "content": f"Research report on {query.topic}",
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
