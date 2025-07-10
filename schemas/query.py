from pydantic import BaseModel

class QueryRequest(BaseModel):
    topic: str
    user_id: str

class QueryResponse(BaseModel):
    success: bool
    report: dict
    cached: bool
