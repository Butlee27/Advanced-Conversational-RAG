from langchain_classic.chains import create_history_aware_retriever


from src.custom_retriever import get_advanced_retriever

from src.llm import get_llm

from src.prompts import get_contextualize_prompt


def get_history_aware():

    llm = get_llm()

    retriever = get_advanced_retriever()

    history_retriever = create_history_aware_retriever(
        llm,
        retriever,
        get_contextualize_prompt(),
    )

    return history_retriever