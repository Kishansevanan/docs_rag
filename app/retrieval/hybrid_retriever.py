from collections import defaultdict
from app.retrieval.vector_retriever import vector_search
from app.retrieval.bm25_retriever import BM25Retriever

RRF_K = 60


def reciprocal_rank_fusion(vector_docs, bm25_docs):

    scores = defaultdict(float)

    for rank, doc in enumerate(vector_docs):
        key = doc.page_content
        scores[key] += 1 / (RRF_K + rank + 1)

    for rank, doc in enumerate(bm25_docs):
        key = doc.page_content
        scores[key] += 1 / (RRF_K + rank + 1)

    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)

    doc_lookup = {doc.page_content: doc for doc in vector_docs + bm25_docs}

    results = [doc_lookup[key] for key, _ in ranked]

    return results


def hybrid_search(query, bm25_retriever, k=5):

    vector_docs = vector_search(query, k=k)

    bm25_docs = bm25_retriever.search(query, k=k)

    fused_docs = reciprocal_rank_fusion(vector_docs, bm25_docs)

    return fused_docs[:k]