from langchain_groq import ChatGroq
from config import (GROQ_API_KEY,llm_model)

def get_llm():
    llm=ChatGroq(
        api_key=GROQ_API_KEY,
        model=llm_model,
        temperature=0)
    
    return llm
