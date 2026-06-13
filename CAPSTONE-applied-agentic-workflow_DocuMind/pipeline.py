# Orchestrates the full DocuMind Workflow
# Ingest → Plan → Retrieve → Work → Critique → Write → Report

import json
from agents import planner_agent, worker_agent, critic_agent, writer_agent
from rag_store import retrieve, ingest_document
from memory import load_memory, add_turn
from config import MAX_RETRIES, CRITIC_THRESHOLD


def run_pipeline(question: str) -> dict:
    print("\n" + "="*50)
    print(f"Question: {question}")
    print("="*50)

    # Step 1: Load Memory
    # Loads whatever Conversation History exists from 'memory.py'
    history = load_memory()
    print(f"Memory: {len(history)} previous turns loaded.")

    # Step 2: Plan
    # Calls the Planner and Prints each Subtask cleanly so you can watch the Decomposition happen in Real Time in the Terminal
    print("\n[Planner] Decomposing question into subtasks...")
    plan = planner_agent(question, history)
    for st in plan.subtasks:
        print(f"  Subtask {st.task_id}: {st.question} [{st.strategy}]")

    # Step 3: Retrieve + Work + Critique per Subtask
    # Core Loop
    # For each Subtask, it Retrieves RAG Chunks, Runs the Worker, then Runs the Critic
    # If the Critic fails it, Feedback gets passed back to the Worker and it retries
    approved_drafts = []

    for subtask in plan.subtasks:
        print(f"\n[Worker] Working on subtask {subtask.task_id}...")

        # Retrieve relevant Chunks from ChromaDB
        rag_chunks = retrieve(subtask.question)
        print(f"  Retrieved {len(rag_chunks)} chunks from vector store.")

        # Reflection Loop
        feedback = ""
        draft = None

        for attempt in range(MAX_RETRIES + 1):
            if attempt > 0:
                print(f"  [Retry {attempt}] Revising based on critic feedback...")

            draft = worker_agent(subtask, rag_chunks, feedback)
            print(f"  Draft produced for subtask {subtask.task_id}.")

            # Critique
            review = critic_agent(draft, rag_chunks)
            print(f"  [Critic] Score: {review.score:.2f} — {'✓ Passed' if review.passed else '✗ Failed'}")

            if review.passed:
                break
            else:
                feedback = review.feedback
                print(f"  [Critic] Feedback: {feedback}")

        approved_drafts.append(draft)

    # Step 4: Write Final Report
    # Only Fires once every Subtask has an approved Draft
    # Synthesizes everything into the final 'FinalReport'
    print("\n[Writer] Synthesizing final report...")
    report = writer_agent(approved_drafts, question)

    # Step 5: Save to Memory
    # Saves the Question and the Report Summary to Memory so that the next Question has Context
    history = add_turn(history, "user", question)
    history = add_turn(history, "assistant", report.summary)

    # Step 6: Save Report to file
    # Creates an "outputs/" Folder automatically and Saves the Full Report as a Clean JSON file (latest_report.json)
    # This is what will be shown in the Portfolio Demo
    output_path = "outputs/latest_report.json"
    import os
    os.makedirs("outputs", exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(report.model_dump(), f, indent=2)
    print(f"\n Report saved to {output_path}")

    return report.model_dump()


def ingest_mode(filepath: str):
    print(f"\nIngesting document: {filepath}")
    ingest_document(filepath)
    print("Document ready for querying.")