from langchain_huggingface import HuggingFaceEmbeddings
from config import embedding_model

def get_embeddings():
    embeddings=HuggingFaceEmbeddings(model_name=embedding_model,
                                     model_kwargs={"device":"cpu"},
                                     encode_kwargs={"normalize_embeddings":True})
    
    return embeddings