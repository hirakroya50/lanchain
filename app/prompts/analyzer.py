
from langchain_core.prompts import ChatPromptTemplate

analyzer_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
        You are a senior software architect.

        Analyze software projects carefully.
        Provide accurate, structured and useful explanations.
        Never invent technical information.
        """
    ),
    (
        "human",
        """
        Analyze the following project:

        Project Name: {project_name}
        Language: {language}
        Description: {description}

        Explain:

        1. What the project does
        2. Its possible architecture
        3. Its main use cases
        4. Its potential technical challenges
        """
    )
])
