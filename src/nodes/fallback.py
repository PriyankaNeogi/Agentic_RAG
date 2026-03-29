def fallback(query, llm):
    prompt = f"""
Answer using general knowledge:

{query}
"""
    return llm.invoke(prompt).content