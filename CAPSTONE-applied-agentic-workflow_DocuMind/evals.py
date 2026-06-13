# Evaluation Framework — Scores the Pipeline's Output Quality
# This is what Separates a Portfolio Project from a toy Demo

import json
import os
from config import client, LLM_MODEL


# Single Response Evaluator
def evaluate_response(question: str, answer: str, context_chunks: list[dict]) -> dict:
    context_text = "\n\n".join([c["text"] for c in context_chunks])

    system = """You are an evaluation judge. Score the answer to the question
based on the provided context. Return ONLY valid JSON:
{
  "groundedness": <0.0-1.0, is the answer supported by the context?>,
  "relevance": <0.0-1.0, does the answer address the question?>,
  "completeness": <0.0-1.0, is the answer thorough?>,
  "overall": <average of the three scores>,
  "verdict": "pass" | "fail",
  "notes": "<one sentence explanation>"
}
Verdict is pass if overall >= 0.7, fail otherwise."""

    user = f"""Question: {question}
Answer: {answer}
Context: {context_text}"""

    response = client.chat.completions.create(
        model=LLM_MODEL,
        temperature=0,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user}
        ]
    )

    return json.loads(response.choices[0].message.content)


# Batch Evaluator: Runs Eval on a Saved Report
def evaluate_report(report_path: str, rag_chunks: list[dict]) -> dict:
    if not os.path.exists(report_path):
        return {"error": f"Report not found: {report_path}"}

    with open(report_path, "r") as f:
        report = json.load(f)

    print(f"\n{'='*50}")
    print("EVALUATION RESULTS")
    print(f"{'='*50}")

    section_scores = []

    for section in report.get("sections", []):
        question = section["question"]
        answer = section["answer"]

        score = evaluate_response(question, answer, rag_chunks)
        section_scores.append(score)

        print(f"\nQ: {question}")
        print(f"  Groundedness : {score['groundedness']:.2f}")
        print(f"  Relevance    : {score['relevance']:.2f}")
        print(f"  Completeness : {score['completeness']:.2f}")
        print(f"  Overall      : {score['overall']:.2f} — {score['verdict'].upper()}")
        print(f"  Notes        : {score['notes']}")

    # Aggregate
    if section_scores:
        avg_overall = sum(s["overall"] for s in section_scores) / len(section_scores)
        passes = sum(1 for s in section_scores if s["verdict"] == "pass")

        print(f"\n{'='*50}")
        print(f"AGGREGATE SCORE  : {avg_overall:.2f}")
        print(f"SECTIONS PASSED  : {passes}/{len(section_scores)}")
        print(f"PIPELINE VERDICT : {'✓ PASS' if avg_overall >= 0.7 else '✗ FAIL'}")
        print(f"{'='*50}\n")

        return {
            "aggregate_score": avg_overall,
            "sections_passed": passes,
            "total_sections": len(section_scores),
            "verdict": "pass" if avg_overall >= 0.7 else "fail",
            "section_scores": section_scores
        }

    return {"error": "No sections found in report."}


# Quick Self-Test: Sanity Check the Pipeline is Working
def run_smoke_test():
    print("\nRunning smoke test...")

    dummy_chunks = [
        {"text": "DocuMind is an AI platform that uses RAG and multi-agent workflows.", "source": "test", "distance": 0.1},
        {"text": "The system supports PDF and TXT document ingestion.", "source": "test", "distance": 0.2}
    ]

    score = evaluate_response(
        question="What does DocuMind do?",
        answer="DocuMind is an AI platform that uses retrieval-augmented generation and multi-agent workflows to answer questions about uploaded documents.",
        context_chunks=dummy_chunks
    )

    print(f"Smoke test score: {score['overall']:.2f} — {score['verdict'].upper()}")
    print(f"Notes: {score['notes']}")
    return score