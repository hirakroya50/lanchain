from pathlib import Path

from langchain_core.documents import Document


ALLOWED_EXTENSIONS = {
    ".py", ".js", ".jsx", ".ts", ".tsx",
    ".java", ".go", ".rs", ".cpp", ".h",
    ".md", ".json", ".yaml", ".yml",
    ".toml", ".sql", ".html", ".css",
}

IGNORED_DIRS = {
    ".git",
    "node_modules",
    ".venv",
    "venv",
    "__pycache__",
    "dist",
    "build",
    ".next",
}

IGNORED_FILES = {
    ".env",
    ".env.local",
    "id_rsa",
    "id_ed25519",
}


def load_repository_documents(repo_path: str):

    root = Path(repo_path)
    documents = []

    for file_path in root.rglob("*"):

        if not file_path.is_file():
            continue

        relative_path = file_path.relative_to(root)

        # Skip unwanted directories
        if any(part in IGNORED_DIRS for part in relative_path.parts):
            continue

        # Skip sensitive filenames
        if file_path.name in IGNORED_FILES:
            continue

        # Only read supported text extensions
        if file_path.suffix.lower() not in ALLOWED_EXTENSIONS:
            continue

        # Avoid huge files
        if file_path.stat().st_size > 200_000:
            continue

        try:
            content = file_path.read_text(
                encoding="utf-8"
            )

            if not content.strip():
                continue

            document = Document(
                page_content=content,
                metadata={
                    "source": str(relative_path),
                    "extension": file_path.suffix,
                }
            )

            documents.append(document)

        except (UnicodeDecodeError, OSError):
            continue

        if len(documents) >= 300:
            break

    return documents