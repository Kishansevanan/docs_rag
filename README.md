# 📚 Docs_RAG - Guardrailed Hybrid RAG for Technical Documentation

This project is a production-style Retrieval-Augmented Generation (RAG) system designed to answer questions over technical documentation such as LangChain and LangGraph docs.

The system retrieves relevant documentation chunks using a hybrid retrieval pipeline (vector search + keyword search) and generates grounded answers using an LLM.
It incorporates retrieval guardrails, citation-aware prompting, and a modular architecture, and is exposed through a production-ready FastAPI service.

The goal of the system is to ensure that answers are accurate, traceable to documentation sources, and resistant to hallucinations.

---

# 🚀 Key Features

- **Hybrid Retrieval Pipeline**
  - Combines semantic vector search with BM25 keyword retrieval
  - Improves recall for technical queries and API references
- **MMR (Max Marginal Relevance) Retrieval**
  - Ensures diversity in retrieved chunks
  - Avoids redundant context in generation
- **Reciprocal Rank Fusion (RRF)**
  - Combines rankings from vector and keyword retrievers
  - Produces more reliable document rankings
- **Guardrails for Safe Generation**
  - Confidence-based refusal when retrieval quality is low
  - Evidence-only prompting to prevent hallucinations
- **Source Citation Support**
  - Retrieved chunks retain document metadata
  - Generated answers reference documentation sources
- **Production-Ready API**
  - FastAPI endpoint for querying the RAG system
  - Structured request and response schemas
  - Swagger UI for interactive testing

---

# 🏗️ Architecture Overview

Technical Documentation (Markdown)\
↓\
Document Ingestion & Chunking\
↓\
Vector Database (Chroma)\
↓\
Hybrid Retrieval Pipeline\
(Vector Search + BM25 + MMR + RRF)\
↓\
Retrieval Guardrails\
↓\
Grounded LLM Generation\
↓\
Answer + Source Citations\
↓\
FastAPI RAG Service

---

# 🛠️ Tech Stack

### Core

- Python 3.10
- FastAPI -- API framework
- Uvicorn -- ASGI server

### RAG & LLM Infrastructure

- LangChain -- orchestration framework
- Groq API -- LLM inference
- ChromaDB -- vector database
- Sentence Transformers -- embedding models

### Retrieval Algorithms

- Vector Similarity Search
- BM25 Keyword Retrieval
- MMR (Max Marginal Relevance)
- Reciprocal Rank Fusion (RRF)

### Data Validation

- Pydantic -- schema validation

### Tooling

- python-dotenv -- environment configuration
- Git -- version control

---
