from app.retrieval.vector_retriever import vector_search
from app.retrieval.bm25_retriever import BM25Retriever
from app.retrieval.hybrid_retriever import hybrid_search
from app.guardrails.confidence import is_low_confidence

from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from app.config import VECTORSTORE_DIR, EMBEDDING_MODEL


def load_all_docs():

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

    docs, metadata = load_all_docs()

    from langchain_core.documents import Document

    documents = [
        Document(page_content=d, metadata=m)
        for d, m in zip(docs, metadata)
    ]

    return BM25Retriever(documents)


def print_results(title, docs):

    print("\n==============================")
    print(title)
    print("==============================")

    for i, d in enumerate(docs):

        print(f"\nResult {i+1}")
        print("SOURCE:", d.metadata.get("source"))

        preview = d.page_content[:200].replace("\n", " ")
        print("CONTENT:", preview)


def run():

    query = "How does LangGraph manage state?"

    print("\nQuery:", query)

    # VECTOR SEARCH
    vector_docs = vector_search(query)

    print_results("Vector Retrieval", vector_docs)

    # BM25 SEARCH
    bm25 = build_bm25()
    bm25_docs = bm25.search(query)

    print_results("BM25 Retrieval", bm25_docs)

    # HYBRID SEARCH
    hybrid_docs = hybrid_search(query, bm25)

    print_results("Hybrid Retrieval (RRF)", hybrid_docs)

    # GUARDRAIL
    if is_low_confidence(hybrid_docs):
        print("\n⚠️ Guardrail triggered: Low confidence retrieval")
    else:
        print("\n✅ Retrieval confidence OK")


if __name__ == "__main__":
    run()