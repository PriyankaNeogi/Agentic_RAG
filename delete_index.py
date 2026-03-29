from pinecone import Pinecone
import os
from dotenv import load_dotenv

load_dotenv()

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

print("Indexes before:", [i.name for i in pc.list_indexes()])

pc.delete_index("agentic-rag")

print("Deleted successfully")

print("Indexes after:", [i.name for i in pc.list_indexes()])