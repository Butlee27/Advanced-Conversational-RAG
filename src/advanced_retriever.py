from src.hybrid_retriever import get_hybrid_retriever
from src.reranker import rerank_document


def get_advanced_retriever(query: str):

    hybrid_retriever = get_hybrid_retriever()

    docs = hybrid_retriever.invoke(query)

    docs = rerank_document(
        query=query,
        documents=docs,
        top_k=3
    )

    return docs