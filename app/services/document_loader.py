
from pathlib import Path

from langchain_core.documents import Document


# File types whose contents we can read as text.
ALLOWED_EXTENSIONS = {
    ".py", ".js", ".jsx", ".ts", ".tsx",
    ".mjs", ".cjs", ".java", ".go", ".rs",
    ".cpp", ".c", ".h", ".hpp",
    ".md", ".txt", ".json", ".yaml", ".yml",
    ".toml", ".ini", ".cfg",
    ".sql", ".html", ".css", ".scss",
    ".sh", ".bash", ".xml",
}

# Directories that should not be scanned.
IGNORED_DIRS = {
    ".git",
    "node_modules",
    ".venv",
    "venv",
    "__pycache__",
    "dist",
    "build",
    ".next",
    ".idea",
    ".pytest_cache",
}

# Sensitive files that must not be loaded.
IGNORED_FILES = {
    ".env",
    "id_rsa",
    "id_ed25519",
    "credentials.json",
}

MAX_FILE_SIZE = 200_000
MAX_DOCUMENTS = 300


def load_repository_documents(repo_path: str) -> list[Document]:
    root = Path(repo_path)

    documents = []

    for file_path in sorted(root.rglob("*")):

        # Only process regular files.
        if not file_path.is_file():
            continue

        # Avoid symbolic links.
        if file_path.is_symlink():
            continue

        relative_path = file_path.relative_to(root)

        # Skip ignored directories.
        if any(part in IGNORED_DIRS for part in relative_path.parts):
            continue

        # Skip sensitive filenames.
        if (
            file_path.name in IGNORED_FILES
            or file_path.name.startswith(".env.")
        ):
            continue

        # Only load supported text file extensions.
        if file_path.suffix.lower() not in ALLOWED_EXTENSIONS:
            continue

        try:
            file_size = file_path.stat().st_size

            # Skip oversized files.
            if file_size > MAX_FILE_SIZE:
                continue

            # Read file contents.
            content = file_path.read_text(encoding="utf-8")

            # Skip empty files.
            if not content.strip():
                continue

            # Convert file contents into a LangChain Document.
            document = Document(
                page_content=content,
                metadata={
                    "source": relative_path.as_posix(),
                    "extension": file_path.suffix.lower(),
                    "size": file_size,
                },
            )

            documents.append(document)

        except (UnicodeDecodeError, OSError):
            # Skip files that cannot be read as UTF-8.
            continue

        # Limit the number of loaded documents.
        if len(documents) >= MAX_DOCUMENTS:
            break

    return documents
