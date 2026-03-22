from graph import AgenticRAG

rag = AgenticRAG()

query = "Explain RAG in very deep detail with examples"

response = rag.run(query)

print("\nFinal Response:\n")
print(response)