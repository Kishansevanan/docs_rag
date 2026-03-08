from langchain_groq import ChatGroq
from app.generation.prompt import SYSTEM_PROMPT

def build_llm():
    llm = ChatGroq(
        model="llama-3.1-8b-instant",
        temperature=0
    )

    return llm


def generate_answer(context, question):
    llm = build_llm()

    prompt = SYSTEM_PROMPT.format(
        context=context,
        question=question
    )

    response = llm.invoke(prompt)

    return response.content