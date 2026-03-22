from nodes.retriever import PineconeRetriever
from nodes.generator import RAGGenerator

retriever = PineconeRetriever()
generator = RAGGenerator()

query = "What are the main components of RAG?"

docs = retriever.retrieve(query)

answer = generator.generate(query, docs)

print("\nFinal Answer:\n")
print(answer)