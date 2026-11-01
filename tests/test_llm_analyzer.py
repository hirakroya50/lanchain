from app.services.git_service import clone_repository
from app.services.document_loader import load_repository_documents
from app.services.text_splitter import split_documents
from app.services.llm_analyzer import analyze_chunk


def test_llm_analyzer():

    repo_url = "https://github.com/hirakroya50/react-ci"

    print("\nCloning repository...")
    repo_path = clone_repository(repo_url)

    print("Loading documents...")
    documents = load_repository_documents(repo_path)

    print("Splitting documents...")
    chunks = split_documents(documents)

    # Select the first actual chunk.
    chunk = chunks[0]

    print("\nAnalyzing:")
    print("File:", chunk.metadata["source"])
    print("Chunk index:", chunk.metadata["chunk_index"])

    result = analyze_chunk(
        project_name="react-ci",
        file_path=chunk.metadata["source"],
        code=chunk.page_content,
    )

    print("\n========== STRUCTURED ANALYSIS ==========")
    print(result.model_dump_json(indent=2))
    print("=========================================")

    assert isinstance(result.summary, str)
    assert isinstance(result.key_components, list)
    assert isinstance(result.technologies, list)
    assert isinstance(result.technical_observations, list)

    print("\nLLM analyzer test passed!")


if __name__ == "__main__":
    test_llm_analyzer()