from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from src.ingestion.ingest import ingest_pipeline
from src.nodes.router import route_query
from src.nodes.retriever import retrieve_docs
from src.nodes.grader import grade_docs
from src.nodes.rewriter import rewrite_query
from src.nodes.generator import generate_answer
from src.nodes.fallback import fallback
from src.nodes.hallucination import check_hallucination
from src.nodes.answer_grader import check_quality

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini")


def run_pipeline(query, vectorstore):
    for i in range(3):
        print(f"\n--- Iteration {i+1} ---")

        # 🔵 ROUTER
        route = route_query(query, llm)
        print("ROUTE:", route)

        # 🔵 DIRECT LLM
        if route == "llm_direct":
            print("Using LLM Direct")
            return fallback(query, llm)

        # 🔵 VECTORSTORE FLOW
        if route == "vectorstore":
            docs = retrieve_docs(query, vectorstore)
            print("DOCS RETRIEVED:", len(docs))

            docs = grade_docs(query, docs, llm)
            print("RELEVANT DOCS:", len(docs))

            if not docs:
                print("No relevant docs → rewriting query...")
                query = rewrite_query(query, llm)
                continue

            answer = generate_answer(query, docs, llm)

            if not check_hallucination(answer, docs, llm):
                print("Hallucination detected → retrying...")
                continue

            if not check_quality(answer, query, llm):
                print("Bad answer quality → retrying...")
                continue

            return answer

        # 🔵 WEB / FALLBACK
        if route == "web_search":
            print("Using fallback/web")
            return fallback(query, llm)

    return "I don't know"


if __name__ == "__main__":
    vectorstore = ingest_pipeline()

    while True:
        q = input("\nQuestion: ")
        if q.lower() == "exit":
            break

        result = run_pipeline(q, vectorstore)
        print("\nAnswer:\n", result)