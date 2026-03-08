def format_context(docs):
    context_parts = []

    for doc in docs:

        source = doc.metadata.get("source", "unknown")

        text = doc.page_content

        context_parts.append(
            f"[SOURCE: {source}]\n{text}"
        )

    return "\n\n".join(context_parts)