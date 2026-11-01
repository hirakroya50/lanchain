
from app.services.git_service import clone_repository
from app.services.document_loader import load_repository_documents


def test_document_loading():
    repo_url = "https://github.com/hirakroya50/react-ci"

    print("\nCloning repository...")
    repo_path = clone_repository(repo_url)

    print("Loading repository documents...")
    documents = load_repository_documents(repo_path)

    print(f"\nTotal documents loaded: {len(documents)}")

    for document in documents:
        print("\n-----------------------------")
        print("Source:", document.metadata["source"])
        print("Extension:", document.metadata["extension"])
        print("Size:", document.metadata["size"])
        print("Content preview:")
        print(document.page_content[:200])

    assert len(documents) > 0, "No documents were loaded"

    assert all(document.page_content.strip() for document in documents)

    print("\nDocument loading test passed!")


if __name__ == "__main__":
    test_document_loading()
