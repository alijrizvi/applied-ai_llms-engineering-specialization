# The Brain - Where the 4 Agents that will Power DocuMind all live!
# Planner -> Worker -> Critic (Reflection Loop) -> Writer

import json
from config import client, LLM_MODEL, MAX_RETRIES, CRITIC_THRESHOLD
from schemas import PlannerOutput, WorkerDraft, CriticReview, FinalReport
from rag_store import retrieve
from memory import build_context_window

import mcp_servers.calculator as calculator_tool
import mcp_servers.web_search as web_search_tool
import mcp_servers.file_manager as file_manager_tool


# Utility: Call the LLM and Parse JSON Response
# Every Agent goes through this function and it generates a JSON response every single time
def call_llm(system_prompt: str, user_prompt: str, history: list[dict] = []) -> str:
    messages = [{"role": "system", "content": system_prompt}]
    if history:
        messages += build_context_window(history)
    messages.append({"role": "user", "content": user_prompt})

    response = client.chat.completions.create(
        model=LLM_MODEL,
        temperature=0,
        response_format={"type": "json_object"},
        messages=messages
    )
    return response.choices[0].message.content


# Agent 1: Planner
# Takes the User's Raw Question and breaks into 1-3 Subtasks, each tagged with a Strategy and a Tool hint
def planner_agent(question: str, history: list[dict] = []) -> PlannerOutput:
    system = """You are a planning agent. Break the user's question into subtasks.
Return ONLY valid JSON matching this exact structure:
{
  "subtasks": [
    {
      "task_id": 1,
      "question": "specific sub-question",
      "strategy": "rag" | "tool" | "both",
      "tool_hint": "web_search" | "calculator" | "file_manager" | null
    }
  ]
}
Keep it to 1-3 subtasks maximum. Be specific."""

    raw = call_llm(system, question, history)
    data = json.loads(raw)
    return PlannerOutput(**data)


# Agent 2: Worker
# Where RAG Context and Tool Output come together - Pulls Retrieved Chunks, Runs the appropriate MCP Tool if needed, and Drafts an Answer
def worker_agent(subtask, rag_chunks: list[dict], feedback: str = "") -> WorkerDraft:
    # Build Context from RAG Chunks
    rag_context = "\n\n".join([
        f"[Source: {c['source']}, relevance: {round(1 - c['distance'], 2)}]\n{c['text']}"
        for c in rag_chunks
    ])

    # Run Tool if needed
    tool_output = ""
    if subtask.strategy in ["tool", "both"] and subtask.tool_hint:
        if subtask.tool_hint == "calculator":
            result = calculator_tool.run({"expression": subtask.question})
        elif subtask.tool_hint == "web_search":
            result = web_search_tool.run({"query": subtask.question})
        elif subtask.tool_hint == "file_manager":
            result = file_manager_tool.run({"action": "list"})
        else:
            result = {}
        tool_output = f"\nTool output ({subtask.tool_hint}):\n{json.dumps(result, indent=2)}"

    feedback_note = f"\nPrevious attempt was rejected. Critic feedback: {feedback}" if feedback else ""

    system = """You are a research agent. Answer the given question using the provided
context and tool output. Be specific and grounded — only use what the context supports.
Return ONLY valid JSON matching this exact structure:
{
  "task_id": <int>,
  "question": "<the question>",
  "draft_answer": "<your answer>",
  "sources": ["<source1>", "<source2>"]
}"""

    user = f"""Question: {subtask.question}

RAG Context:
{rag_context}
{tool_output}
{feedback_note}"""

    raw = call_llm(system, user)
    data = json.loads(raw)
    return WorkerDraft(**data)


# Agent 3: Critic (if the Critic rejects the draft, the feedback gets passed back in and the Worker tries again with specific guidance)
# Scores the Draft on Groundedness, Completeness, and Clarity (Averaged into a Single Float value)
# Returns 'passed: false' with Specific Feedback. The Pipeline will then Loop back to the Worker
def critic_agent(draft: WorkerDraft, rag_chunks: list[dict]) -> CriticReview:
    rag_context = "\n\n".join([c["text"] for c in rag_chunks])

    system = """You are a quality critic agent. Review the draft answer against the
retrieved context. Score it from 0.0 to 1.0 on three criteria:
- Groundedness: is it supported by the context? (not hallucinated)
- Completeness: does it fully answer the question?
- Clarity: is it clear and specific?

Average the three scores for the final score.
Return ONLY valid JSON matching this exact structure:
{
  "task_id": <int>,
  "score": <float between 0.0 and 1.0>,
  "passed": <true if score >= 0.7, else false>,
  "feedback": "<specific improvement notes if failed, empty string if passed>"
}"""

    user = f"""Question: {draft.question}
Draft answer: {draft.draft_answer}

Retrieved context:
{rag_context}"""

    raw = call_llm(system, user)
    data = json.loads(raw)
    return CriticReview(**data)


# Agent 4: Writer
# Only Runs once ALL Drafts are Approved
# Synthesizes everything into a Clean 'FinalReport' Pydantic object with a Title, Executive Summary, Sections, and Sources
def writer_agent(approved_drafts: list[WorkerDraft], question: str) -> FinalReport:
    drafts_text = "\n\n".join([
        f"Q: {d.question}\nA: {d.draft_answer}"
        for d in approved_drafts
    ])

    all_sources = list(set([s for d in approved_drafts for s in d.sources]))

    system = """You are a professional report writer. Synthesize the approved research
into a clean, readable final report.
Return ONLY valid JSON matching this exact structure:
{
  "title": "<report title>",
  "summary": "<2-3 sentence executive summary>",
  "sections": [
    {"question": "<question>", "answer": "<answer>"}
  ],
  "sources_used": ["<source1>", "<source2>"]
}"""

    user = f"""Original question: {question}

Approved research:
{drafts_text}

Sources: {all_sources}"""

    raw = call_llm(system, user)
    data = json.loads(raw)
    return FinalReport(**data)