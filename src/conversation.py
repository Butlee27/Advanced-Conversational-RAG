from langchain_core.runnables.history import RunnableWithMessageHistory

from src.chains import get_rag_chain
from src.history import get_session_history


def get_conversation():

    chain = get_rag_chain()

    conversation = RunnableWithMessageHistory(
        chain,
        get_session_history,
        input_messages_key="input",
        history_messages_key="chat_history",
        output_messages_key="answer",
    )

    return conversation