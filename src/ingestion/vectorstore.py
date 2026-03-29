import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Pinecone as PineconeStore
from pinecone import Pinecone, ServerlessSpec

load_dotenv()


def create_vectorstore(chunks):
    print("Creating Pinecone vector DB...")

    pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

    index_name = os.getenv("PINECONE_INDEX_NAME", "rag-index")

    existing_indexes = [i.name for i in pc.list_indexes()]

    if index_name not in existing_indexes:
        print("Creating Pinecone index...")

        pc.create_index(
            name=index_name,
            dimension=1536,
            metric="cosine",
            spec=ServerlessSpec(
                cloud="aws",
                region=os.getenv("PINECONE_ENV", "us-east-1")
            )
        )

    index = pc.Index(index_name)

    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

    vectorstore = PineconeStore(
        index=index,
        embedding=embeddings,
        text_key="text"
    )

    # 🔥 CRITICAL FIX: Always reset data
    print(" Resetting Pinecone index...")
    index.delete(delete_all=True)

    print("Adding fresh documents to Pinecone...")
    vectorstore.add_documents(chunks)

    return vectorstore