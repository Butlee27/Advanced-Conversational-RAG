from langchain_text_splitters import RecursiveCharacterTextSplitter
from config import(chunk_overlap,chunk_size)

def split_documents(documents):
    text_splitter=RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    chunks=text_splitter.split_documents(documents)
    return chunks