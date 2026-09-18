import hashlib
import os
import time
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)

import streamlit as st

from src.llm import get_llm
from src.conversation import get_conversation
from src.indexer import build_vector_database
from src.loader import pdf_exists
from src.guardrails import (detect_prompt_injection,
                            detect_pii,
                            mask_pii,
                            detect_unsafe_request,
                            check_groundedness,
                            sanitize_output,
                            fallback_response,)
st.set_page_config(
    page_title="Advanced Conversational RAG",
    page_icon="📚",
    layout="wide",
)

st.title("📚 Advanced Conversational RAG")
st.markdown("Ask questions about your uploaded PDF documents.")

if "conversation" not in st.session_state:
    st.session_state.conversation = None

if (st.session_state.conversation is None and pdf_exists()):
    st.session_state.conversation=get_conversation()

if "messages" not in st.session_state:
    st.session_state.messages = []

if "uploaded_hashes" not in st.session_state:
    st.session_state.uploaded_hashes = set()

with st.sidebar:

    st.header("📂 Upload PDF")

    uploaded_file = st.file_uploader(
        "Choose a PDF",
        type=["pdf"],
    )

    if uploaded_file is not None:

        file_bytes = uploaded_file.getvalue()
        file_hash = hashlib.sha256(file_bytes).hexdigest()

        if file_hash not in st.session_state.uploaded_hashes:
            os.makedirs("data/pdfs", exist_ok=True)
            save_path = os.path.join(
                "data",
                "pdfs",
                uploaded_file.name,
            )

            with open(save_path, "wb") as f:
                f.write(file_bytes)

            with st.spinner("Processing PDF..."):
                try:

                    build_vector_database()
                    st.session_state.conversation = get_conversation()
                    st.session_state.uploaded_hashes.add(file_hash)
                    st.success("✅ PDF processed successfully!")
                except Exception as e:
                    st.error(f"❌ Failed to process PDF\n\n{e}")

        else:
            pass
    st.divider()
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()


for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

question = st.chat_input("Ask a question about your documents...")
if question:
    request_start=time.perf_counter()
    request_status="success"
    logger.info("Query received")
    if st.session_state.conversation is None:
        st.warning("⚠️ Please upload a PDF before asking a question.")
        st.stop()
    if detect_prompt_injection(question):
        logger.warning("Prompt injection detected")
        st.warning(
            "⚠️ I can't process requests that attempt to override my instructions."
        )
        st.stop()
    if detect_unsafe_request(question):
        logger.warning("Unsafe request detected")
        st.warning(
            "⚠️ I can't process that request."
        )
        st.stop()

    if detect_pii(question):
        logger.info("PII detected and masked")
        question = mask_pii(question)


    st.session_state.messages.append(
        {
            "role": "user",
            "content": question,
        }
    )

    with st.chat_message("user"):
        st.markdown(question)
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                rag_start = time.perf_counter()
                response = st.session_state.conversation.invoke(
                    {
                        "input": question
                    },
                    config={
                        "configurable": {
                            "session_id": "harish"
                        }
                    },
                )
                rag_latency = time.perf_counter() - rag_start

                logger.info(
                    "RAG completed | latency=%.2f seconds",
                    rag_latency
                )

            
                usage = {}

                if hasattr(response, "usage_metadata"):
                    usage = response.usage_metadata

                elif isinstance(response, dict):
                    usage = response.get("usage_metadata", {})

                if usage:
                    logger.info(
                        "Token usage | input=%s | output=%s | total=%s",
                        usage.get("input_tokens"),
                        usage.get("output_tokens"),
                        usage.get("total_tokens"),
                    )


                else:
                    logger.info("Token usage metadata not available")

                answer = response["answer"]
                documents = response["context"]
                logger.info(
                    "Retrieved documents | count=%d",
                    len(documents)
                )

                context="\n\n".join(
                    doc.page_content
                    for doc in documents
                )

                llm=get_llm()

                grounded_start = time.perf_counter()
                grounded=check_groundedness(
                    llm,
                    answer,
                    context
                )

                grounded_latency = time.perf_counter() - grounded_start

                logger.info(
                    "Groundedness check completed | grounded=%s | latency=%.2f seconds",
                    grounded,
                    grounded_latency
                )

                if not grounded:
                    logger.warning(
                        "Groundedness check failed | retrying generation"
                    )

                    retry_prompt = f"""
                Answer the question using ONLY the provided context.

                Context:
                {context}

                Question:
                {question}

                Do not add information that is not present
                in the context.

                If the answer is not present in the context,
                say that you don't know.
                """

                    retry_response = llm.invoke(retry_prompt)

                    answer = retry_response.content

                    grounded = check_groundedness(
                        llm,
                        answer,
                        context
                    )

                    logger.info(
                        "Retry groundedness result | grounded=%s",
                        grounded
                    )

                    if not grounded:
                        logger.warning(
                            "Retry failed | using fallback response"
                        )
                        answer=fallback_response()

                answer=sanitize_output(answer)

                


            except Exception as e:
                request_status="error"
                logger.exception(
                    "RAG request failed | error=%s",
                    str(e)
                )

                answer = f"❌ Error:\n\n{e}"
                documents = []

            st.markdown(answer)

            if documents:
                st.markdown("---")
                st.markdown("### 📄 Sources")

                shown = set()

                for doc in documents:

                    source = os.path.basename(
                        doc.metadata["source"]
                    )
                    source = source.replace(".docx.pdf", ".pdf")
                    page = doc.metadata["page"] + 1
                    key = (source, page)
                    if key not in shown:
                        shown.add(key)
                        with st.expander(
                            f"📄 {source} - Page {page}"
                        ):
                            st.write(doc.page_content)

    total_latency = time.perf_counter() - request_start

    logger.info(
        "Request completed | total_latency=%.2f seconds",
        request_status,
        total_latency
    )
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer,
        }
    )