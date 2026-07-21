from langchain_community.retrievers import BM25Retriever

from src.loader import load_documents
from src.splitter import split_documents

from config import search_k


def get_bm25_retriever():

    documents = load_documents()

    chunks = split_documents(documents)

    retriever = BM25Retriever.from_documents(chunks)

    retriever.k = search_k

    return retriever