import tempfile
from pathlib import Path
from git import Repo


def clone_repository(repo_url: str) -> str:

    if not repo_url.startswith("https://github.com/"):
        raise ValueError("Only GitHub HTTPS URLs are supported")

    repo_path = tempfile.mkdtemp(prefix="repolens-")

    Repo.clone_from(
        repo_url,
        repo_path,
        depth=1,
        multi_options=["--single-branch"],
    )

    return repo_path