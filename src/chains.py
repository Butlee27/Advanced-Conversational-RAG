from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import(create_stuff_documents_chain)

from src.llm import get_llm
from src.prompts import get_rag_prompt
from src.history_retriever import get_history_aware

def get_rag_chain():
    llm=get_llm()
    retriever=get_history_aware()
    prompt=get_rag_prompt()

    document_chain=create_stuff_documents_chain(
        llm,
        prompt
    )

    rag_chain=create_retrieval_chain(
        retriever,
        document_chain
    )

    return rag_chain