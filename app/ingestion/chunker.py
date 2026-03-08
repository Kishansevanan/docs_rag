from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.config import CHUNK_SIZE, CHUNK_OVERLAP

def chunk_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n## ", "\n### ", "\n\n", "\n", " "]
    )

    chunks = splitter.split_documents(documents)

    # add chunk ids for citation
    for i, chunk in enumerate(chunks):
        chunk.metadata["chunk_id"] = i

    return chunks