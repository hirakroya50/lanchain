from typing import Literal, Optional

from pydantic import BaseModel, Field


class JobStatus(BaseModel):

    analysis_id: str

    status: Literal[
        "pending",
        "running",
        "completed",
        "failed"
    ]

    progress: int = Field(
        ge=0,
        le=100,
        description="Analysis progress percentage"
    )

    message: str

    error: Optional[str] = None