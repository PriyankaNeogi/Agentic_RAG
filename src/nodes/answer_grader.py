def check_quality(answer, query, llm):
    prompt = f"""
Does this answer fully address the question?

Question: {query}
Answer: {answer}

Reply yes or no.
"""

    result = llm.invoke(prompt).content.lower()
    return "yes" in result