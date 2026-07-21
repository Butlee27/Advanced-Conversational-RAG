import os

from langchain_community.document_loaders import PyPDFLoader

from config import pdf_directory


def load_documents():
    documents = []

    pdf_files = [
        file for file in os.listdir(pdf_directory)
        if file.endswith(".pdf")
    ]

    if not pdf_files:
        raise FileNotFoundError("No PDF files found.")

    for pdf in pdf_files:

        pdf_path = os.path.join(pdf_directory, pdf)

        loader = PyPDFLoader(pdf_path)

        docs = loader.load()

        documents.extend(docs)

    return documents


def pdf_exists():

    if not os.path.exists(pdf_directory):
        return False

    pdf_files = [
        file for file in os.listdir(pdf_directory)
        if file.endswith(".pdf")
    ]

    return 