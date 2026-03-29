from dotenv import load_dotenv
from src.config import load_config

from src.ingestion.loader import load_documents
from src.ingestion.chunker import chunk_documents
from src.ingestion.vectorstore import create_vectorstore

import os

load_dotenv()
config = load_config()


def ingest_pipeline():
    pdf_path = config["paths"]["pdf_path"]

    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    print(f"\nStarting ingestion: {pdf_path}")

    docs = load_documents(pdf_path)

    chunks = chunk_documents(
        docs,
        chunk_size=config["chunking"]["chunk_size"],
        chunk_overlap=config["chunking"]["chunk_overlap"]
    )

    #  CRITICAL FIX: add text metadata
    for chunk in chunks:
        chunk.metadata["text"] = chunk.page_content

    vectorstore = create_vectorstore(chunks)

    print("\nIngestion complete")

    return vectorstore