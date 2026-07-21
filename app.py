import hashlib
import os
import streamlit as st

from src.conversation import get_conversation
from src.indexer import build_vector_database
from src.loader import pdf_exists

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

                answer = response["answer"]
                documents = response["context"]

            except Exception as e:

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
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer,
        }
    )