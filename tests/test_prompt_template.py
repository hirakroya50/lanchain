from app.llm.client import llm
from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are an expert software architect."
    ),
    (
        "human",
        "Explain the purpose of this file in 3 sentences.\n\n"
        "File: {file_path}\n\n"
        "Code:\n{code}"
    )
])

chain = prompt | llm


def test_prompt_template():

    response = chain.invoke({
        "file_path": "src/auth.py",
        "code": """
def login_user(email, password):
    user = find_user(email)
    if verify_password(password, user.password):
        return create_access_token(user.id)
"""
    })

    print("\n========== FILE ANALYSIS ==========")
    print(response.content)
    print("===================================")

    assert response.content


if __name__ == "__main__":
    test_prompt_template()