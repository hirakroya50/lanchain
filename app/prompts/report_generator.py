from langchain_core.prompts import ChatPromptTemplate

report_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
        You are a senior software architect.

        Your task is to generate a comprehensive technical
        report about a software repository using the
        provided individual code analysis results.

        Rules:
        1. Use only information supported by the findings.
        2. Never invent technologies, databases, or features.
        3. Combine related findings instead of repeating them.
        4. Identify the overall architecture from the available evidence.
        5. If information is insufficient, clearly mention that.
        6. Distinguish confirmed facts from potential improvements.
        7. Keep the report technically useful and concise.
        """
    ),
    (
        "human",
        """
        Generate a technical report for this repository.

        Project name: {project_name}

        Individual chunk analysis findings:

        {findings}

        Consolidate these findings into one complete
        repository-level technical report.
        """
    )
])