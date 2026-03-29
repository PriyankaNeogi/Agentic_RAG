def check_hallucination(answer, docs, llm):
    context = "\n".join([doc.page_content for doc in docs])

    prompt = f"""
Is this answer supported by the context?

Answer: {answer}
Context: {context}

Reply yes or no.
"""

    result = llm.invoke(prompt).content.lower()
    return "yes" in result