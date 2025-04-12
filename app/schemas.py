from pydantic import BaseModel, HttpUrl
from typing import List, Optional

class RepositoryAnalysisRequest(BaseModel):
    repo_url: HttpUrl
    branch: Optional[str] = "main"
    file_filter: Optional[List[str]] = None

class CodeAnalysis(BaseModel):
    summary: str
    tests: str
    review: str
    improvements: List[str]

class HealthCheck(BaseModel):
    status: str
    mistral_available: bool