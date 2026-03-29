def generate_answer(query, docs, llm):
    context = "\n\n".join(
        [f"(Page {doc.metadata.get('page', 'N/A')}): {doc.page_content}" for doc in docs]
    )

    prompt = f"""
You MUST answer using ONLY the provided context.

- Be specific
- Refer to document content clearly
- Include page references

Context:
{context}

Question: {query}
"""

    return llm.invoke(prompt).content