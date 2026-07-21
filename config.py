import os
from dotenv import load_dotenv
load_dotenv()

GROQ_API_KEY=os.getenv("GROQ_API_KEY")

llm_model="llama-3.3-70b-versatile"
embedding_model="BAAI/bge-small-en-v1.5"
cross_encoder_model="cross-encoder/ms-marco-MiniLM-L-6-v2"

chunk_size=800
chunk_overlap=200

search_k=3

vector_k=10
BM25_top_k=10
final_top_k=5

pdf_directory="data/pdfs"
chroma_db_path="chroma_db"
App_Titel="Advanced Hybrid Conversational RAG"
App_icon = "🤖"

