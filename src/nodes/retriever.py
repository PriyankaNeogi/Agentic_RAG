def retrieve_docs(query, vectorstore):
    docs = vectorstore.similarity_search(query, k=5)
    print(f"Retrieved {len(docs)} docs")
    return docs