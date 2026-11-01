from app.services.git_service import clone_repository
from app.services.document_loader import load_repository_documents
from app.services.text_splitter import split_documents
from app.services.llm_analyzer import analyze_chunk
from app.services.report_generator import generate_project_report


def test_report_generator():

    repo_url = "https://github.com/hirakroya50/react-ci"

    print("\nCloning repository...")
    repo_path = clone_repository(repo_url)

    print("Loading documents...")
    documents = load_repository_documents(repo_path)

    print("Splitting documents...")
    chunks = split_documents(documents)

    # Analyze a maximum of 5 chunks for this test.
    chunks_to_analyze = chunks[:5]

    chunk_analyses = []

    print("\nAnalyzing chunks...")

    for chunk in chunks_to_analyze:

        analysis = analyze_chunk(
            project_name="react-ci",
            file_path=chunk.metadata["source"],
            code=chunk.page_content,
        )

        analysis_data = analysis.model_dump()

        analysis_data["file_path"] = chunk.metadata["source"]
        analysis_data["chunk_index"] = chunk.metadata["chunk_index"]

        chunk_analyses.append(analysis_data)

    print("\nGenerating project report...")

    report = generate_project_report(
        project_name="react-ci",
        chunk_analyses=chunk_analyses,
    )

    print("\n========== PROJECT REPORT ==========")
    print(report.model_dump_json(indent=2))
    print("====================================")

    assert report.project_name == "react-ci"
    assert isinstance(report.overview, str)
    assert isinstance(report.languages, list)
    assert isinstance(report.frameworks, list)
    assert isinstance(report.architecture, str)
    assert isinstance(report.database, list)
    assert isinstance(report.main_features, list)
    assert isinstance(report.technical_challenges, list)
    assert isinstance(report.improvements, list)

    print("\nProject report generator test passed!")


if __name__ == "__main__":
    test_report_generator()