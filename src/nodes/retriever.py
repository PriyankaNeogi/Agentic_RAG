import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from dotenv import load_dotenv
from pinecone import Pinecone
from langchain_openai import OpenAIEmbeddings
from config import load_config

load_dotenv()
config = load_config()


class PineconeRetriever:
    def __init__(self):
        self.pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
        self.index = self.pc.Index(config["pinecone"]["index_name"])
        self.embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
        self.top_k = config["retrieval"]["top_k"]

    def retrieve(self, query: str):
        query_embedding = self.embeddings.embed_query(query)

        results = self.index.query(
            vector=query_embedding,
            top_k=self.top_k,
            include_metadata=True
        )

        documents = []

        for match in results["matches"]:
            metadata = match.get("metadata", {})

            text = metadata.get("text") or str(metadata)

            documents.append({
                "text": text,
                "score": match.get("score", 0),
                "source": metadata.get("source", ""),
                "page": metadata.get("page", -1)
            })

        return documents