# Entry point for DocuMind — AI Knowledge Agent Platform
# This is what we Actually Run: "python main.py"

import os
import sys
from pipeline import run_pipeline, ingest_mode
from memory import clear_memory, load_memory
from evals import evaluate_report, run_smoke_test
from rag_store import retrieve


def print_banner():
    print("""
╔══════════════════════════════════════════════╗
║         DocuMind — AI Knowledge Agent        ║
║     RAG · Multi-Agent · MCP · Memory         ║
╚══════════════════════════════════════════════╝
""")


def print_menu():
    print("""
What would you like to do?

  1. Ingest a document
  2. Ask a question
  3. Evaluate last report
  4. Run smoke test
  5. View memory
  6. Clear memory
  7. Exit
""")


def main():
    print_banner()

    while True:
        print_menu()
        choice = input("Enter choice (1-7): ").strip()

        # Option 1: Ingest
        if choice == "1":
            path = input("\nEnter file path (PDF or TXT): ").strip()
            if os.path.exists(path):
                ingest_mode(path)
            else:
                print(f"File not found: {path}")

        # Option 2: Ask
        elif choice == "2":
            question = input("\nAsk your question: ").strip()
            if not question:
                print("Please enter a question.")
                continue

            report = run_pipeline(question)

            print(f"\n{'='*50}")
            print(f"FINAL REPORT: {report['title']}")
            print(f"{'='*50}")
            print(f"\nSummary:\n{report['summary']}")
            print(f"\nSections:")
            for section in report["sections"]:
                print(f"\n  Q: {section['question']}")
                print(f"  A: {section['answer']}")
            print(f"\nSources: {', '.join(report['sources_used'])}")
            print(f"{'='*50}\n")

        # Option 3: Evaluate
        elif choice == "3":
            report_path = "outputs/latest_report.json"
            if not os.path.exists(report_path):
                print("\nNo report found. Ask a question first (option 2).")
                continue

            question = input("\nWhat was your original question? (for context retrieval): ").strip()
            chunks = retrieve(question)
            evaluate_report(report_path, chunks)

        # Option 4: Smoke Test
        elif choice == "4":
            run_smoke_test()

        # Option 5: View Memory
        elif choice == "5":
            history = load_memory()
            if not history:
                print("\nNo memory yet.")
            else:
                print(f"\nSession memory ({len(history)} turns):\n")
                for turn in history:
                    role = turn["role"].upper()
                    content = turn["content"][:200]
                    timestamp = turn.get("timestamp", "")
                    print(f"  [{timestamp[:19]}] {role}: {content}...")

        # Option 6: Clear Memory
        elif choice == "6":
            confirm = input("\nClear all memory? (y/n): ").strip().lower()
            if confirm == "y":
                clear_memory()

        # Option 7: Exit
        elif choice == "7":
            print("\nAlhamdulillah — session complete. Goodbye! 👋\n")
            sys.exit(0)

        else:
            print("Invalid choice. Please enter 1-7.")


if __name__ == "__main__":
    main()