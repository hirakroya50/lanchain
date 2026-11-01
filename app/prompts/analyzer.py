from langchain_core.prompts import ChatPromptTemplate


analyzer_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
        You are a senior software engineer and software architect.

        Analyze the provided source code carefully.

        Rules:
        1. Only report information supported by the provided code.
        2. Never invent functions, technologies, or features.
        3. If information is insufficient, clearly say so.
        4. Identify important functions, classes, and components.
        5. Identify technologies only when there is evidence.
        6. Provide concise but technically useful observations.
        """
    ),
    (
        "human",
        """
        Analyze the following repository code chunk.

        Repository: {project_name}
        File path: {file_path}

        Source code:

        ```text
        {code}
        ```

        Provide:
        1. A summary of this code.
        2. Its key functions, classes, and components.
        3. Technologies and libraries identified.
        4. Important technical observations.
        """
    )
])