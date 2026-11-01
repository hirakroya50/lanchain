
from pydantic import BaseModel, Field


class RepositoryReport(BaseModel):

    project_name: str = Field(description="Name of the project")

    overview: str = Field(description="What the project does")

    languages: list[str] = Field(
        description="Programming languages used"
    )

    frameworks: list[str] = Field(
        description="Frameworks and libraries used"
    )

    architecture: str = Field(
        description="Explanation of the project architecture"
    )

    database: list[str] = Field(
        description="Databases used or identified"
    )

    main_features: list[str] = Field(
        description="Main project features"
    )

    technical_challenges: list[str] = Field(
        description="Potential technical challenges"
    )

    improvements: list[str] = Field(
        description="Suggested improvements"
    )
