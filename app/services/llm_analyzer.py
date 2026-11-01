from app.llm.client import llm
from app.prompts.analyzer import analyzer_prompt
from app.schemas.chunk_analysis import ChunkAnalysis


# Convert the LLM into a structured-output model.
structured_llm = llm.with_structured_output(ChunkAnalysis)


# Connect prompt and LLM.
analyzer_chain = analyzer_prompt | structured_llm


def analyze_chunk(
    project_name: str,
    file_path: str,
    code: str,
) -> ChunkAnalysis:

    result = analyzer_chain.invoke({
        "project_name": project_name,
        "file_path": file_path,
        "code": code,
    })

    return result