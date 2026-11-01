
from pathlib import Path
from collections import Counter

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

IGNORED_FILES = {
    ".env",
    ".env.local",
    "id_rsa",
    "id_ed25519",
}

MAX_FILE_SIZE = 500_000

IMPORTANT_FILES = {
    "README.md",
    "package.json",
    "pyproject.toml",
    "requirements.txt",
    "Cargo.toml",
    "go.mod",
    "build.gradle",
    "build.gradle.kts",
    "settings.gradle",
    "pom.xml",
    "Dockerfile",
    "docker-compose.yml",
    "Makefile",
}


def create_repository_inventory(repo_path: str):
    root = Path(repo_path)

    files = []
    ignored = []

    for path in sorted(root.rglob("*")):

        if not path.is_file():
            continue

        relative_path = path.relative_to(root)
        relative = str(relative_path)

        # Ignore symlinks for safety
        if path.is_symlink():
            ignored.append({
                "path": relative,
                "reason": "symlink"
            })
            continue

        # Ignore unwanted directories
        if any(part in IGNORED_DIRS for part in relative_path.parts):
            continue

        # Ignore sensitive filenames
        if path.name in IGNORED_FILES:
            ignored.append({
                "path": relative,
                "reason": "sensitive filename"
            })
            continue

        try:
            size = path.stat().st_size
        except OSError:
            ignored.append({
                "path": relative,
                "reason": "cannot access file"
            })
            continue

        # Ignore oversized files
        if size > MAX_FILE_SIZE:
            ignored.append({
                "path": relative,
                "reason": "file too large"
            })
            continue

        extension = path.suffix.lower() or "[no extension]"

        files.append({
            "path": relative,
            "name": path.name,
            "extension": extension,
            "size": size,
            "is_important": path.name in IMPORTANT_FILES,
        })

    extension_counts = Counter(
        file["extension"] for file in files
    )

    return {
        "repository_path": str(root),
        "total_files": len(files) + len(ignored),
        "supported_files": len(files),
        "ignored_files": len(ignored),
        "extension_counts": dict(extension_counts),
        "important_files": [
            file for file in files
            if file["is_important"]
        ],
        "files": files,
        "ignored": ignored,
    }
