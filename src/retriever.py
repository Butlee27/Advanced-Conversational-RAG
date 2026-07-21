"""
Creates the document retriever.
"""

from config import search_k
from src.vectordb import load_vector_store


def get_retriever():

    vectorstore = load_vector_store()

    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={
            "k": search_k
        }
    )

    return retriever