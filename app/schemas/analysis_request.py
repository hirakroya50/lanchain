from pydantic import BaseModel, Field, field_validator
from urllib.parse import urlparse


class AnalysisRequest(BaseModel):

    repo_url: str = Field(
        ...,
        description="GitHub repository URL",
        examples=["https://github.com/username/repository"]
    )

    @field_validator("repo_url")
    @classmethod
    def validate_github_url(cls, value: str) -> str:

        value = value.strip()

        parsed_url = urlparse(value)

        if parsed_url.scheme != "https":
            raise ValueError("Only HTTPS URLs are supported")

        if parsed_url.netloc.lower() != "github.com":
            raise ValueError("Only GitHub repository URLs are allowed")

        parts = [
            part for part in parsed_url.path.strip("/").split("/")
            if part
        ]

        if len(parts) != 2:
            raise ValueError("Invalid GitHub repository URL")

        if any(part in {".", ".."} for part in parts):
            raise ValueError("Invalid repository URL")

        return value.rstrip("/")