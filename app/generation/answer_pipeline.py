from app.retrieval.hybrid_retriever import hybrid_search
from app.retrieval.bm25_retriever import BM25Retriever
from app.guardrails.confidence import is_low_confidence

from app.generation.citations import format_context
from app.generation.generator import generate_answer

from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

from app.config import VECTORSTORE_DIR, EMBEDDING_MODEL

def load_docs():
    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL
    )

    vectorstore = Chroma(
        persist_directory=VECTORSTORE_DIR,
        embedding_function=embeddings
    )

    data = vectorstore.get()

    return data["documents"], data["metadatas"]


def build_bm25():
    docs, metadata = load_docs()

    from langchain_core.documents import Document

    documents = [
        Document(page_content=d, metadata=m)
        for d, m in zip(docs, metadata)
    ]

    return BM25Retriever(documents)


def answer_query(query):
    bm25 = build_bm25()

    docs = hybrid_search(query, bm25)

    if is_low_confidence(docs):

        return {
            "answer": "The documentation does not contain enough information to answer this question.",
            "sources": []
        }

    context = format_context(docs)

    answer = generate_answer(context, query)

    sources = list({d.metadata.get("source") for d in docs})

    return {
        "answer": answer,
        "sources": sources
    }