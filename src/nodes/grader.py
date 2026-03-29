def grade_docs(query, docs, llm):
    relevant_docs = []

    for doc in docs:
        prompt = f"""
Is this document helpful in answering the question?

Question: {query}

Document:
{doc.page_content}

Reply only 'yes' or 'no'.
"""

        result = llm.invoke(prompt).content.lower()

        if "yes" in result:
            relevant_docs.append(doc)

    return relevant_docs