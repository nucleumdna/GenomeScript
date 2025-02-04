from pydantic import BaseModel
from typing import Optional, Any, List
from datetime import datetime

class GenomicQuery(BaseModel):
    query_id: str
    script: str
    parameters: Optional[dict] = None

class AnalysisResult(BaseModel):
    query_id: str
    result: Any
    execution_time: float
    status: str

class UserCredentials(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str 