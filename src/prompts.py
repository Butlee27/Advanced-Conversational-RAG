from langchain_core.prompts import (ChatPromptTemplate,MessagesPlaceholder)


def get_rag_prompt():
    prompt=ChatPromptTemplate.from_messages([(
        "system",
        """
        You are a helpful AI assistant.
        Answer only using the provided context.
        If the answer is not present in the context,
        reply:
        "I don't know based on the provided documents."
        Context:
        {context}
    """,),
    MessagesPlaceholder("chat_history"),
    ("human","{input}")])

    return prompt



def get_contextualize_prompt():

    prompt = ChatPromptTemplate.from_messages(
        [

            (
                "system",

                """
Given the chat history and the latest user question,

rewrite the latest question into a standalone question.

Do NOT answer it.

Only rewrite it.
                """,
            ),

            MessagesPlaceholder(
                "chat_history"
            ),

            (
                "human",
                "{input}"
            ),

        ]
    )

    return prompt
