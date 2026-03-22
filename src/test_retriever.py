from nodes.retriever import PineconeRetriever

retriever = PineconeRetriever()

query = "What is the main contribution of the research paper?"

docs = retriever.retrieve(query)

print("\nTop Results:\n")

for i, doc in enumerate(docs):
    print(f"Result {i+1}")
    print(f"Score: {doc['score']}")
    print(f"Page: {doc['page']}")
    print(f"Text: {doc['text'][:200]}")
    print("-" * 50)