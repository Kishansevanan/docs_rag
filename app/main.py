from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(
    title="Docs RAG",
    description="RAG system for technical documentation",
    version="1.0"
)

app.include_router(router)