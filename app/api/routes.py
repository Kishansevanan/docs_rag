from fastapi import APIRouter

from app.schemas.qa_schema import QuestionRequest, AnswerResponse
from app.generation.answer_pipeline import answer_query

router = APIRouter()

@router.post("/ask", response_model=AnswerResponse)
async def ask_question(request: QuestionRequest):

    result = answer_query(request.question)

    return AnswerResponse(
        answer=result["answer"],
        sources=result["sources"]
    )