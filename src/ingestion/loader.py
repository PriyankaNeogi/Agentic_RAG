from langchain_community.document_loaders import PyPDFLoader


def load_documents(pdf_path):
    loader = PyPDFLoader(pdf_path)
    docs = loader.load()

    print(f"Loaded {len(docs)} pages")

    return docs