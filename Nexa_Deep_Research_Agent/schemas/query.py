from pydantic import BaseModel
from typing import Optional

class QueryRequest(BaseModel):
    topic: str
    user_id: str
    pass_type: Optional[str] = "full"   # "full", "half", or "direct"
    model: Optional[str] = "DeepSeek-R1-open"  # Selected OpenRouter model

class QueryResponse(BaseModel):
    success: bool
    report: dict
    cached: bool
