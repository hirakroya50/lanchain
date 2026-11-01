from pydantic import BaseModel, Field


class ChunkAnalysis(BaseModel):

    summary: str = Field(
        description="A concise explanation of what this code chunk does"
    )

    key_components: list[str] = Field(
        description="Important functions, classes, modules, or components identified"
    )

    technologies: list[str] = Field(
        description="Technologies, libraries, and frameworks explicitly identified"
    )

    technical_observations: list[str] = Field(
        description="Important technical observations supported by the provided code"
    )