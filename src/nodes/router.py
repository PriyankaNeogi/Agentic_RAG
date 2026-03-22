import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


class QueryRouter:
    def __init__(self):
        # Strong indicators → use your PDF (vectorstore)
        self.vector_keywords = [
            "rag",
            "retrieval",
            "generation",
            "augmentation",
            "paper",
            "research",
            "study",
            "components",
            "method",
            "framework"
        ]

        # Strong indicators → need external/latest info
        self.web_keywords = [
            "latest",
            "news",
            "today",
            "recent",
            "current",
            "2024",
            "2025"
        ]

    def route(self, query: str):
        q = query.lower()

        # 1. Vectorstore (highest priority)
        if any(word in q for word in self.vector_keywords):
            return "vectorstore"

        # 2. Web search
        if any(word in q for word in self.web_keywords):
            return "web_search"

        # 3. Default → LLM direct
        return "llm_direct"