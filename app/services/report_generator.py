from app.llm.client import llm
from app.prompts.report_generator import report_prompt
from app.schemas.report import RepositoryReport

# Convert the LLM into a structured-output model.
structured_llm = llm.with_structured_output(RepositoryReport)

# Connect the prompt and LLM.
report_chain = report_prompt | structured_llm


def generate_project_report(
    project_name: str,
    chunk_analyses: list[dict],
) -> RepositoryReport:

    # Convert individual analyses into readable text.
    findings = "\n\n".join(
        [
            f"""
            File: {analysis["file_path"]}
            Chunk: {analysis["chunk_index"]}

            Summary:
            {analysis["summary"]}

            Key components:
            {", ".join(analysis["key_components"])}

            Technologies:
            {", ".join(analysis["technologies"])}

            Technical observations:
            {", ".join(analysis["technical_observations"])}
            """
            for analysis in chunk_analyses
        ]
    )

    # Generate the consolidated project report.
    report = report_chain.invoke({
        "project_name": project_name,
        "findings": findings,
    })

    return report