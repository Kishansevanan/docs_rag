from pathlib import Path
from langchain_community.document_loaders import TextLoader
from langchain_core.documents import Document

def load_markdown_docs(base_path: str) -> list[Document]:
    documents = []

    for md_file in Path(base_path).rglob("*.md"):
        loader = TextLoader(str(md_file), encoding="utf-8")
        docs = loader.load()

        for doc in docs:
            doc.metadata = {
                "source": md_file.name,
                "path": str(md_file),
                "doc_type": "markdown"
            }
            documents.append(doc)

    return documents