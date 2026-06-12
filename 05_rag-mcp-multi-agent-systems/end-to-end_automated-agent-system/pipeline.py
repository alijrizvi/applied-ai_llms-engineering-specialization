# Here, we bring all the Components of our System together into a Single Orchestrated Workflow
# Orchestration

import time

from agents import planner_agent, researcher_agent, analyst_agent, writer_agent
from rag_store import retrieve_rag
from tools import fetch_tool, summarize_tool, store_tool
from email_trigger import check_email
from email_sender import send_email_gmail_api

## Executes the full sequence: Planning the task, Fetching external data, Retrieving RAG results, Generating research, Analyzing it, Summarizing it, Storing the output, and finally Producing a polished report
def run_pipeline(task, url):
    task = task[:400] # Avoid Over-sized Prompts

    plan = planner_agent(task)
    fetched = fetch_tool(url)
    rag = retrieve_rag(task)
    research = researcher_agent(task, fetched, rag)
    analysis = analyst_agent(research)
    summary = summarize_tool(analysis)
    store_tool(summary)
    final_report = writer_agent(summary)

    return final_report


## Runs from Console Input
def manual_mode():
    print("Enter task:")
    task = input("-> ")

    print("Enter URL:")
    url = input("-> ")

    result = run_pipeline(task, url)
    print("\n=== FINAL REPORT ===\n")
    print(result)


## The System continuously listens for new unread emails
## When a Message arrives, it Builds a task from the Email content, Runs the pipeline, and Sends an automated reply back to the sender using the Gmail API
## Reacts to incoming emails (i.e., is event-driven)
def email_mode():
    print("Email agent running... waiting for new emails... \n")

    while True:
        new = check_email()
        if new:
            body = new["body"][:500]
            task = new["subject"] + "\n" + body
            sender = new["from"]

            run_pipeline(task, "https://example.com")

            send_email_gmail_api(
                sender,
                "Message received",
                "Thanks! Your message has been received and processed."
            )

            print(f"Replied to {sender}\n")

        time.sleep(5)


## Acts as the central controller, coordinating all Agents, Tools, and Triggers to run a Complete End-to-End Automated Workflow
if __name__ == "__main__":
    print("Choose mode:")
    print("1. Manual Input Mode")
    print("2. Email Trigger Mode")

    mode = input("-> ")
    if mode == "1":
        manual_mode()
    else:
        email_mode()