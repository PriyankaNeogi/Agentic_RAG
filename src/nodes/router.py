def route_query(query, llm):
    query_lower = query.lower()

    # Force document queries
    if any(word in query_lower for word in ["document", "paper", "pdf"]):
        return "vectorstore"

    prompt = f"""
Classify the query into:
- llm_direct
- vectorstore
- web_search

Query: {query}

Return only one word.
"""

    result = llm.invoke(prompt).content.lower()

    if "web" in result:
        return "web_search"
    elif "llm" in result:
        return "llm_direct"
    else:
        return "vectorstore"