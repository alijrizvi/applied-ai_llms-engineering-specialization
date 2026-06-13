# Conversational Memory - Persists Session History so the Agent remembers what was discussed earlier in the same Session

import json
import os
from datetime import datetime

MEMORY_FILE = "session_memory.json"

# Reads the Session History from a JSON file on disk. If no file exists yet (fresh Session) = Returns an Empty List
def load_memory() -> list[dict]:
    if not os.path.exists(MEMORY_FILE):
        return []
    with open(MEMORY_FILE, "r") as f:
        return json.load(f)

# Writes the Content history back to disk after every turn. Makes the program persistent
# Because of this, if we Stop and then Restart the program, it picks up where it left off
def save_memory(history: list[dict]):
    with open(MEMORY_FILE, "w") as f:
        json.dump(history, f, indent=2)

# Appends one Message (either from the User or the Assistant) to the History with a Timestamp, then Saves immediately
def add_turn(history: list[dict], role: str, content: str) -> list[dict]:
    history.append({
        "role": role,
        "content": content,
        "timestamp": datetime.now().isoformat()
    })
    save_memory(history)
    return history

# Takes the last 6 turns of convo, Strips the tiemstamps, and thus manages Memory of the LLM in Stages
def build_context_window(history: list[dict], max_turns: int = 6) -> list[dict]:
    # Only send the last 'n' turns to the LLM to stay within Context Limits
    # Strip Timestamps — OpenAI only wants "role" + "content"
    recent = history[-max_turns:]
    return [{"role": t["role"], "content": t["content"]} for t in recent]

# Wipes the Session file.
def clear_memory():
    if os.path.exists(MEMORY_FILE):
        os.remove(MEMORY_FILE)
    print("Memory cleared.")