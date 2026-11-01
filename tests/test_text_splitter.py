
from langchain_core.documents import Document

from app.services.text_splitter import split_documents


def test_document_chunking():
    # Create a sample document with enough text to produce multiple chunks.
    content = "\n\n".join([
    """
    User Authentication:
    The application uses JWT tokens for authentication.
    Passwords are hashed using bcrypt before storing them.
    Users can register, log in, and reset their passwords.
    """ * 10,

    """
    Database Architecture:
    PostgreSQL is used as the primary database.
    Prisma ORM manages database queries.
    Database migrations are handled through Prisma migrate.
    """ * 10,

    """
    Payment Processing:
    Stripe handles payment processing.
    Webhooks verify successful transactions.
    Failed payments are recorded for retry.
    """ * 10,

    """
    API Architecture:
    Express.js provides REST API endpoints.
    Middleware handles authentication and request validation.
    Error responses follow a consistent JSON structure.
    """ * 10,
    ])

    documents = [
        Document(
            page_content=content,
            metadata={
                "source": "src/App.tsx",
                "extension": ".tsx",
            },
        )
    ]

    chunks = split_documents(documents)

    print("Original documents:", len(documents))
    print("Generated chunks:", len(chunks))

    for chunk in chunks[:5]:
        print("\n-------------------------")
        print("Chunk index:", chunk.metadata["chunk_index"])
        print("Start index:", chunk.metadata["start_index"])
        print("Full content:")
        print(chunk.page_content)

    assert len(chunks) > 1, "Document was not split into multiple chunks"

    assert all(
        chunk.metadata["source"] == "src/App.tsx"
        for chunk in chunks
    )

    assert all(
        len(chunk.page_content) <= 1500
        for chunk in chunks
    )

    print("\nDocument chunking test passed!")


if __name__ == "__main__":
    test_document_chunking()
