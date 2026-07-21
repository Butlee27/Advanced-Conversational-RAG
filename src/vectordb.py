from langchain_chroma import Chroma
from config import chroma_db_path
from src.embeddings import get_embeddings

def create_vector_store(chunks):
    embeddings=get_embeddings()
    vectorstore=Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=chroma_db_path
    )
    return vectorstore

def load_vector_store():
    embeddings=get_embeddings()
    vectorstore=Chroma(
        persist_directory=chroma_db_path,
        embedding_function=embeddings
    )
    return vectorstore