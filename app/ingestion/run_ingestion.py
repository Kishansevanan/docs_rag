from app.ingestion.loader import load_markdown_docs
from app.ingestion.chunker import chunk_documents
from app.ingestion.vectorstore import build_or_load_vectorstore

def run():
    docs = []
    docs += load_markdown_docs("data/raw_docs/langchain")
    docs += load_markdown_docs("data/raw_docs/langgraph")

    chunks = chunk_documents(docs)
    vectorstore = build_or_load_vectorstore(chunks)

    print(f"Ingested {len(chunks)} chunks into vector store")


if __name__ == "__main__":
    run()