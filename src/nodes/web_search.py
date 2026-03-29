from tavily import TavilyClient
import os
from src.config import load_config

config = load_config()

def tavily_search(query):
    client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

    response = client.search(
        query=query,
        max_results=config["tavily"]["max_results"]
    )

    return [r["content"] for r in response["results"]]