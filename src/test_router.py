from nodes.router import QueryRouter

router = QueryRouter()

queries = [
    "What is machine learning?",
    "What are the main components of RAG?",
    "Latest news about AI in 2025"
]

for q in queries:
    route = router.route(q)
    print(f"\nQuery: {q}")
    print(f"Route: {route}")