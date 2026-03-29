def check_hallucination(answer, docs, llm):
    context = "\n\n".join([d.page_content for d in docs])

    prompt = f"""
Check if the answer is supported by the context.

If mostly supported, return YES.
If completely unrelated, return NO.

Context:
{context}

Answer:
{answer}
"""
    response = llm.invoke(prompt)

    return "NO" not in response.content.upper()


def check_quality(query, answer, llm):
    prompt = f"""
Check if the answer reasonably answers the question.

Even if not perfect, return YES if it is useful.

Question: {query}
Answer: {answer}
"""
    response = llm.invoke(prompt)

    return "NO" not in response.content.upper()