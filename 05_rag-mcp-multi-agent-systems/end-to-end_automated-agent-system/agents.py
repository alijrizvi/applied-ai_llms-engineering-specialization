# Here, we Define the Core Intelligence of our System
## LLM Logic only

from config import client, MODEL_NAME


def ask_openai(prompt: str) -> str:
    res = client.chat.completions.create(
        model=MODEL_NAME,
        max_tokens=120,
        temperature=0,
        messages=[{"role": "user", "content": prompt}]
    )
    return res.choices[0].message.content


def planner_agent(task: str):
    return ask_openai(
        f"Create a clear 3-step plan for this task. Keep it short and concise:\n{task}"
    )

## Combines the Fetched Content + RAG results into a Research note
def researcher_agent(task, fetched, rag):
    return ask_openai(
        f"""
Task:
{task}

Fetched:
{fetched}

RAG:
{rag}

Write a 3-4 sentence research note combining everything.
"""
    )


def analyst_agent(research_note: str):
    return ask_openai(
        f"Turn this research note into 3 bullet points:\n\n{research_note}"
    )


def writer_agent(summary: str):
    return ask_openai(
        f"Write a short final report in 3 sentences on this Summary:\n\n{summary}"
    )
