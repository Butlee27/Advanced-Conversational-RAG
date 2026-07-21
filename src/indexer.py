from src.loader import load_documents
from src.splitter import split_documents
from src.embeddings import get_embeddings
from src.vectordb import create_vector_store


def build_vector_database():

    documents = load_documents()

    chunks = split_documents(documents)

    embedding_model = get_embeddings()

    create_vector_store(
        chunks
    )