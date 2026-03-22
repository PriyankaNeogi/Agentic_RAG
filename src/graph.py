import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), ".")))

from nodes.router import QueryRouter
from nodes.retriever import PineconeRetriever
from nodes.generator import RAGGenerator
from nodes.grader import RAGGrader


class AgenticRAG:
    def __init__(self):
        self.router = QueryRouter()
        self.retriever = PineconeRetriever()
        self.generator = RAGGenerator()
        self.grader = RAGGrader()
        self.max_retries = 3

    def run(self, query: str):
        for attempt in range(self.max_retries):

            print(f"\nAttempt {attempt + 1}")

            route = self.router.route(query)
            print(f"Route: {route}")

            # 🔹 Case 1: Direct LLM
            if route == "llm_direct":
                return self.generator.generate(query, [])

            # 🔹 Case 2: Vectorstore
            elif route == "vectorstore":
                docs = self.retriever.retrieve(query)

                if not docs:
                    print("No documents found, retrying...")
                    continue  # ✅ inside loop

                answer = self.generator.generate(query, docs)

                # 🔥 Try grading safely
                try:
                    hallucination_ok = self.grader.hallucination_check(answer, docs)
                    quality_ok = self.grader.quality_check(query, answer)
                except Exception as e:
                    print("Grader error, returning answer")
                    return answer

                # ✅ If both checks pass
                if hallucination_ok and quality_ok:
                    return answer

                print("Grader flagged issue")

                # 🔥 Last attempt → return anyway
                if attempt == self.max_retries - 1:
                    print("Returning last attempt anyway")
                    return answer

                continue  # ✅ properly inside loop

            # 🔹 Case 3: Web fallback
            elif route == "web_search":
                return "Web search not implemented"

        return "Failed after retries"