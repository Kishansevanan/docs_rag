from rank_bm25 import BM25Okapi

class BM25Retriever:
    def __init__(self, documents):

        self.documents = documents
        self.corpus = [doc.page_content.split() for doc in documents]

        self.bm25 = BM25Okapi(self.corpus)

    def search(self, query, k=5):

        tokens = query.split()

        scores = self.bm25.get_scores(tokens)

        ranked = sorted(
            zip(self.documents, scores),
            key=lambda x: x[1],
            reverse=True
        )

        return [doc for doc, _ in ranked[:k]]