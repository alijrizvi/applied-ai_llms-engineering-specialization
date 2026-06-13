# MCP Tool Server 2 - File Manager
# Handles Reading and Listing files the User has uploaded

import os

ALLOWED_EXTENSIONS = [".pdf", ".txt", ".csv", ".md"]
UPLOAD_DIR = "./uploads"


def list_files() -> dict:
    """List all available uploaded files."""
    if not os.path.exists(UPLOAD_DIR):
        return {"tool": "file_manager", "action": "list", "files": [], "status": "no uploads folder found"}
    
    files = [
        f for f in os.listdir(UPLOAD_DIR)
        if os.path.splitext(f)[1].lower() in ALLOWED_EXTENSIONS
    ]
    return {
        "tool": "file_manager",
        "action": "list",
        "files": files,
        "status": "success"
    }


def read_file(filename: str) -> dict:
    """Reads the first 1000 characters of a text file."""
    filepath = os.path.join(UPLOAD_DIR, filename)

    if not os.path.exists(filepath):
        return {"tool": "file_manager", "action": "read", "content": None, "status": "file not found"}

    ext = os.path.splitext(filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        return {"tool": "file_manager", "action": "read", "content": None, "status": "unsupported file type"}

    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read(1000)
        return {
            "tool": "file_manager",
            "action": "read",
            "filename": filename,
            "content": content,
            "status": "success"
        }
    except Exception as e:
        return {"tool": "file_manager", "action": "read", "content": None, "status": f"error: {str(e)}"}


def run(params: dict) -> dict:
    action = params.get("action", "list")
    if action == "list":
        return list_files()
    elif action == "read":
        return read_file(params.get("filename", ""))
    else:
        return {"tool": "file_manager", "status": "unknown action"}