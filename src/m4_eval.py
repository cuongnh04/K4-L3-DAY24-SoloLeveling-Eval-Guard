"""RAGAS 0.1 evaluator: real metrics, explicit model provenance, no synthetic fallback."""
import os
from types import SimpleNamespace


def evaluate_ragas(questions, answers, contexts, ground_truths):
    # Load Torch DLLs before Arrow/RAGAS on Windows to avoid c10 initialization failure.
    import torch
    from datasets import Dataset
    from langchain_openai import ChatOpenAI
    from langchain_community.embeddings import HuggingFaceEmbeddings
    from ragas import evaluate
    from ragas.metrics import faithfulness, answer_relevancy, context_precision, context_recall
    from ragas.run_config import RunConfig
    from config import GENERATION_MODEL, EMBEDDING_MODEL

    if not questions or len({len(questions), len(answers), len(contexts), len(ground_truths)}) != 1:
        raise ValueError("Evaluation lists must be nonempty and aligned")
    model = os.getenv("EVALUATOR_MODEL", GENERATION_MODEL)
    from langchain_core.rate_limiters import InMemoryRateLimiter
    interval = float(os.getenv("API_INTERVAL_SECONDS", "0"))
    limiter = InMemoryRateLimiter(requests_per_second=1 / interval, max_bucket_size=1) if interval else None
    llm = ChatOpenAI(model=model, temperature=0, timeout=120, max_retries=3, rate_limiter=limiter)
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL,
                                      encode_kwargs={"normalize_embeddings": True})
    dataset = Dataset.from_dict(dict(question=questions, answer=answers,
                                    contexts=contexts, ground_truth=ground_truths))
    metrics = [faithfulness, answer_relevancy, context_precision, context_recall]
    # Gemini's endpoint accepts one candidate; use one generated relevance question.
    answer_relevancy.strictness = 1
    result = evaluate(dataset, metrics=metrics, llm=llm, embeddings=embeddings,
                      raise_exceptions=True,
                      run_config=RunConfig(max_workers=4, timeout=180, max_retries=3))
    rows = [SimpleNamespace(**{m.name: float(row[m.name]) for m in metrics})
            for row in result.to_pandas().to_dict("records")]
    return {"per_question": rows,
            "metadata": {"evaluator_models": [model, EMBEDDING_MODEL]}}
