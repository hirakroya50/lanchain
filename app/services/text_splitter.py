
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document


def split_documents(
    documents: list[Document],
) -> list[Document]:

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1500,
        chunk_overlap=200,
        separators=[
            "\n\n",
            "\n",
            " ",
            "",
        ],
        add_start_index=True,
    )

    chunks = splitter.split_documents(documents)

    # Give every chunk an index within its source file.
    chunk_counts = {}

    for chunk in chunks:
        source = chunk.metadata.get("source", "unknown")

        chunk_index = chunk_counts.get(source, 0)

        chunk.metadata["chunk_index"] = chunk_index

        chunk_counts[source] = chunk_index + 1

    return chunks
