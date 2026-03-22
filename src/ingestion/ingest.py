import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from pinecone import Pinecone, ServerlessSpec
from config import load_config

load_dotenv()
config = load_config()


def ingest_to_pinecone():
    pdf_path = config["paths"]["pdf_path"]

    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF not found at: {pdf_path}")

    print(f"Loading PDF: {pdf_path}")

    loader = PyPDFLoader(pdf_path)
    pages = list(loader.lazy_load())

    print(f"Loaded {len(pages)} pages")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=config["chunking"]["chunk_size"],
        chunk_overlap=config["chunking"]["chunk_overlap"]
    )

    chunks = splitter.split_documents(pages)

    print(f"Created {len(chunks)} chunks")

    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

    pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

    index_name = config["pinecone"]["index_name"]

    # Create index if not exists
    if index_name not in [i["name"] for i in pc.list_indexes()]:
        pc.create_index(
            name=index_name,
            dimension=config["pinecone"]["dimension"],
            metric=config["pinecone"]["metric"],
            spec=ServerlessSpec(
                cloud="aws",
                region=os.getenv("PINECONE_ENV")
            )
        )

    index = pc.Index(index_name)

    print("Uploading vectors to Pinecone...")

    vectors = []
    for i, chunk in enumerate(chunks):
        embedding = embeddings.embed_query(chunk.page_content)

        vectors.append({
            "id": str(i),
            "values": embedding,
            "metadata": {
                "text": chunk.page_content,
                "source": chunk.metadata.get("source", ""),
                "page": chunk.metadata.get("page", -1)
            }
        })

    index.upsert(vectors)

    print("Data successfully stored in Pinecone")
    print("Ingestion complete")


if __name__ == "__main__":
    ingest_to_pinecone()