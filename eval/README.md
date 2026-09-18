# RAG Evaluation

## Files

- `dataset.py` — 10 evaluation questions and ground-truth answers based on Unit V of the uploaded Deep Learning notes.
- `run_evaluation.py` — calls the existing `src.conversation.get_conversation()` and records the generated answers and retrieved contexts.
- `results/raw_results.json` — created after running the evaluator.

## Run

From the existing Advanced Conversational RAG project root:

```bash
python eval/run_evaluation.py
```

This first stage only collects the data needed for evaluation. Ragas metrics will be added after we verify that the raw answers and retrieved contexts are being captured correctly.
