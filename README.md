# 📚 Advanced Conversational RAG

An advanced Retrieval-Augmented Generation (RAG) application that allows users to upload PDF documents and ask questions conversationally.

The project combines document retrieval, conversational memory, reranking, guardrails, evaluation, observability, and Docker containerization.

## 🚀 Features

- 📄 PDF document upload
- 🔎 Semantic document retrieval
- 🔀 Hybrid retrieval / reranking
- 💬 Conversational RAG with session memory
- 🛡️ Prompt-injection detection
- 🔐 PII detection and masking
- 🚫 Unsafe-request detection
- 🎯 Groundedness checking
- 🧹 Output sanitization
- 🔄 Fallback responses for unsupported answers
- 📊 RAG evaluation using Ragas
- 📈 Evaluation metrics:
  - Faithfulness
  - Context Precision
  - Context Recall
  - Answer Relevancy
  - Answer Correctness
- 📝 Application logging and latency monitoring
- 🐳 Dockerized deployment
- 📚 Source/page references for retrieved documents

## 🏗️ Architecture

```text
                    ┌───────────────┐
                    │   User / PDF  │
                    └───────┬───────┘
                            │
                            ▼
                    ┌───────────────┐
                    │ Streamlit App │
                    └───────┬───────┘
                            │
                            ▼
                    ┌───────────────┐
                    │  Guardrails   │
                    │ PII / Safety  │
                    │ Injection     │
                    └───────┬───────┘
                            │
                            ▼
                    ┌───────────────┐
                    │ RAG Pipeline  │
                    └───────┬───────┘
                            │
                    ┌───────▼────────┐
                    │ Vector Database │
                    │    ChromaDB     │
                    └───────┬────────┘
                            │
                            ▼
                    ┌───────────────┐
                    │   Retriever   │
                    │ + Reranking   │
                    └───────┬───────┘
                            │
                            ▼
                    ┌───────────────┐
                    │   Groq LLM    │
                    └───────┬───────┘
                            │
                            ▼
                    ┌───────────────┐
                    │ Groundedness  │
                    │    Check      │
                    └───────┬───────┘
                            │
                            ▼
                    ┌───────────────┐
                    │    Answer     │
                    │ + Sources     │
                    └───────────────┘

🛠️ Tech Stack
Python
Streamlit
LangChain
ChromaDB
Sentence Transformers
Hugging Face
Groq
Ragas
PyPDF
Docker
📁 Project Structure
Advanced Rag/
│
├── app.py
├── config.py
├── requirements.txt
├── requirements-docker.txt
├── Dockerfile
├── .dockerignore
├── .gitignore
├── README.md
│
├── src/
│   ├── __init__.py
│   ├── conversation.py
│   ├── embeddings.py
│   ├── guardrails.py
│   ├── indexer.py
│   ├── llm.py
│   └── loader.py
│
├── eval/
│   ├── dataset.py
│   └── evaluate_ragas.py
│
├── test/
│   └── test_guardrails.py
│
└── data/
    └── pdfs/
🔐 Environment Variables

Create a .env file:

GROQ_API_KEY=your_groq_api_key

Never commit .env or API keys to GitHub.

▶️ Run Locally

Create and activate your environment, then install dependencies:

pip install -r requirements.txt

Run:

streamlit run app.py
🐳 Run with Docker

Build the image:

docker build -t advanced-rag .

Run:

docker run --env-file .env -p 8501:8501 advanced-rag

Open:

http://localhost:8501
📊 Evaluation

The RAG pipeline is evaluated using Ragas.

The project evaluates:

Faithfulness — whether the answer is supported by the retrieved context.
Context Precision — whether the retrieved context is relevant to the question.
Context Recall — whether the required information was retrieved.
Answer Relevancy — whether the answer addresses the user's question.
Answer Correctness — how closely the generated answer matches the expected answer.

Example evaluation results from the development dataset:

Faithfulness       : 0.9000
Context Precision  : 1.0000
Context Recall     : 1.0000
Answer Relevancy   : 0.9131
Answer Correctness : 0.8529

These values are evaluation results for the project's test dataset and can vary with the dataset, model, and evaluation run.

🛡️ Guardrails

The application includes:

Prompt injection detection
PII detection
PII masking
Unsafe request detection
Groundedness verification
Output sanitization
Fallback responses
📈 Observability

Application logging captures important runtime information such as:

RAG latency
Number of retrieved documents
Groundedness-check latency
Total request latency
Request completion status

Example:

RAG completed | latency=10.09 seconds
Retrieved documents | count=3
Groundedness check completed | grounded=True | latency=0.57 seconds
Request completed | total_latency=10.70 seconds
👨‍💻 Project Goal

This project demonstrates how a production-oriented conversational RAG system can combine:

RAG
+ Conversational Memory
+ Retrieval/Reranking
+ Guardrails
+ Evaluation
+ Observability
+ Docker

to build a more reliable and deployable GenAI application.