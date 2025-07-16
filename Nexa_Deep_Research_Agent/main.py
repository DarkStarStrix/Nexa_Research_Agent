from fastapi import FastAPI
from api.routes import router
from config import REDIS_URL
import aioredis
from services.helix_client import HelixClient
import datetime
from fastapi.responses import JSONResponse

app = FastAPI()

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

@app.get("/health")
async def health_check():
    return JSONResponse({
        "status": "healthy",
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "version": "1.0.0"
    })
