from langchain_classic.retrievers import EnsembleRetriever
from src.retriever import get_retriever
from src.bm25 import get_bm25_retriever

def get_hybrid_retriever():
    vector_retriever=get_retriever()
    bm25_retriever=get_bm25_retriever()

    hybrid_retriever=EnsembleRetriever(
        retrievers=[vector_retriever,bm25_retriever],
        weights=[0.5,0.5]
    )

    return hybrid_retriever