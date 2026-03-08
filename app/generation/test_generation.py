from app.generation.answer_pipeline import answer_query

def run():
    query = "How does LangGraph manage state?"

    result = answer_query(query)

    print("\nQUESTION:")
    print(query)

    print("\nANSWER:")
    print(result["answer"])

    print("\nSOURCES:")
    for s in result["sources"]:
        print("-", s)


if __name__ == "__main__":
    run()