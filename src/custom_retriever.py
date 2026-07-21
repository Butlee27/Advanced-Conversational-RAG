from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever
from pydantic import Field
from typing import Any

from src.hybrid_retriever import get_hybrid_retriever
from src.reranker import rerank_document


class AdvancedRetriever(BaseRetriever):

    hybrid_retriever: Any = Field(default_factory=get_hybrid_retriever)
    top_k: int = 3

    def _get_relevant_documents(
        self,
        query: str,
    ) -> list[Document]:

        docs = self.hybrid_retriever.invoke(query)

        docs = rerank_document(
            query=query,
            documents=docs,
            top_k=self.top_k,
        )

        return docs
    
def get_advanced_retriever():
    return AdvancedRetriever()