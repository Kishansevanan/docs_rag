import os
from dotenv import load_dotenv

load_dotenv()

# Embeddings
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# Vector store
VECTORSTORE_DIR = "data/vector_store/langchain_langgraph"

# Chunking
CHUNK_SIZE = 800
CHUNK_OVERLAP = 150