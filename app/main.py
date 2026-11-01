
from app.services.git_service import clone_repository
from app.services.repository_inventory import (
    create_repository_inventory,
)


def main():
    repo_url = input("Enter GitHub repository URL: ")

    print("\n[1] Cloning repository...")

    repo_path = clone_repository(repo_url)

    print("\n[2] Creating repository inventory...")

    inventory = create_repository_inventory(repo_path)

    print("\n========== REPOSITORY INVENTORY ==========")

    print("Total files:", inventory["total_files"])
    print("Supported files:", inventory["supported_files"])
    print("Ignored files:", inventory["ignored_files"])

    print("\n========== FILE EXTENSIONS ==========")

    for extension, count in sorted(
        inventory["extension_counts"].items()
    ):
        print(f"{extension}: {count}")

    print("\n========== IMPORTANT FILES ==========")

    for file in inventory["important_files"]:
        print(file["path"])

    print("\n========== FIRST 20 FILES ==========")

    for file in inventory["files"][:20]:
        print(
            file["path"],
            f"({file['size']} bytes)"
        )


if __name__ == "__main__":
    main()
