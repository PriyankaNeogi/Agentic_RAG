from src.config import PINECONE_API_KEY, PINECONE_INDEX_NAME
from pinecone import Pinecone
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Pinecone as LangchainPinecone


def create_vectorstore(chunks):
    embeddings = OpenAIEmbeddings()

    pc = Pinecone(api_key=PINECONE_API_KEY)
    pc.Index(PINECONE_INDEX_NAME)

    db = LangchainPinecone.from_documents(
        documents=chunks,
        embedding=embeddings,
        index_name=PINECONE_INDEX_NAME
    )

    return db