from typing import Optional

from pydantic import BaseModel
from app.schemas.report import RepositoryReport


class AnalysisCreatedResponse(BaseModel):
    analysis_id: str
    status: str
    message: str


class AnalysisResultResponse(BaseModel):
    repository: str
    documents_loaded: int
    chunks_created: int
    chunks_analyzed: int
    project_report: RepositoryReport


class AnalysisJobResponse(BaseModel):
    analysis_id: str
    status: str
    progress: int
    message: str
    result: Optional[AnalysisResultResponse] = None
    error: Optional[str] = None