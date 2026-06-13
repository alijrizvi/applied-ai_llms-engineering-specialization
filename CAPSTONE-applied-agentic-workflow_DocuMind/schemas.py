# Pydantic Schemas - Define the exact Shape of Data flowing between Agents
# This is what separates a Production System from a Demo: Typed, Validated Data

from pydantic import BaseModel
from typing import Optional, List

# --- Planner output ---
class Subtask(BaseModel):
    task_id: int
    question: str
    strategy: str
    tool_hint: Optional[str] = None

class PlannerOutput(BaseModel):
    subtasks: List[Subtask]

# --- Worker output ---
class WorkerDraft(BaseModel):
    task_id: int
    question: str
    draft_answer: str
    sources: List[str]

# --- Critic output ---
class CriticReview(BaseModel):
    task_id: int
    score: float # 0.0 to 1.0
    passed: bool # "True" if Score >= THRESHOLD
    feedback: str

# --- Final report ---
class FinalReport(BaseModel):
    title: str
    summary: str
    sections: List[dict]
    sources_used: List[str]