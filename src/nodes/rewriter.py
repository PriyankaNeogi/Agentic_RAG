def rewrite_query(query, llm):
    prompt = f"""
Rewrite this query to improve document retrieval:

{query}
"""
    return llm.invoke(prompt).content.strip()