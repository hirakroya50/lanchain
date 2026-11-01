from app.llm.client import llm


def test_llm_connection():

    response = llm.invoke(
        "Explain what a REST API is in 3 sentences."
    )

    print("\n========== LLM RESPONSE ==========")
    print(response.content)
    print("==================================")

    assert response.content
    print("\nLLM test passed!")


if __name__ == "__main__":
    test_llm_connection()