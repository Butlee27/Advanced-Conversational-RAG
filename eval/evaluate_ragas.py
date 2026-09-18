import sys
import types
import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from langchain_google_vertexai import ChatVertexAI

vertexai_module = types.ModuleType(
    "langchain_community.chat_models.vertexai"
)

vertexai_module.ChatVertexAI = ChatVertexAI

sys.modules[
    "langchain_community.chat_models.vertexai"
] = vertexai_module


from datasets import Dataset

from ragas import evaluate
from ragas.metrics import (faithfulness,
                           context_precision,
                           context_recall,
                           answer_relevancy,
                           answer_correctness)
from ragas.llms import LangchainLLMWrapper
from ragas.embeddings import LangchainEmbeddingsWrapper
from src.embeddings import get_embeddings
from src.llm import get_llm

def load_results():

    path = (
        PROJECT_ROOT
        / "eval"
        / "results"
        / "raw_results.json"
    )

    with open(
        path,
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)


def main():

    results = load_results()
    #results=results[:2]

    data = {
        "question": [
            item["question"]
            for item in results
        ],

        "answer": [
            item["answer"]
            for item in results
        ],

        "contexts": [
            [
                context["page_content"]
                for context in item["contexts"]
            ]
            for item in results
        ],

        "ground_truth": [
            item["ground_truth"]
            for item in results
        ],
    }

    dataset = Dataset.from_dict(data)

    llm = get_llm()

    evaluator_llm = LangchainLLMWrapper(llm)
    embeddings=get_embeddings()
    evaluator_embeddings=LangchainEmbeddingsWrapper(
        embeddings
    )

    print("Running Ragas evaluation...")

    result = evaluate(
        dataset,
        metrics=[
            faithfulness,
            context_precision,
            context_recall,
            answer_relevancy,
            answer_correctness
        ],
        llm=evaluator_llm,
        embeddings=evaluator_embeddings,
        raise_exceptions=False
    )

    print("\nEvaluation Result:")
    print(result)

if __name__ == "__main__":
    main()