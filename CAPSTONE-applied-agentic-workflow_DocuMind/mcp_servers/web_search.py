# MCP Tool Server 3 — Web Search
# Gives the Agent access to current Information beyond its Training Data

import requests
import os
from dotenv import load_dotenv

load_dotenv()

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")


def search(query: str, max_results: int = 3) -> dict:
    """
    Searches the web using Tavily API and returns top results.
    Falls back to a helpful message if no API key is configured.
    """
    if not TAVILY_API_KEY:
        return {
            "tool": "web_search",
            "query": query,
            "results": [],
            "status": "no TAVILY_API_KEY found in .env — web search disabled"
        }

    try:
        response = requests.post(
            "https://api.tavily.com/search",
            json={
                "api_key": TAVILY_API_KEY,
                "query": query,
                "max_results": max_results,
                "search_depth": "basic"
            },
            timeout=10
        )
        data = response.json()
        results = [
            {"title": r["title"], "url": r["url"], "snippet": r["content"][:300]}
            for r in data.get("results", [])
        ]
        return {
            "tool": "web_search",
            "query": query,
            "results": results,
            "status": "success"
        }
    except Exception as e:
        return {
            "tool": "web_search",
            "query": query,
            "results": [],
            "status": f"error: {str(e)}"
        }


def run(params: dict) -> dict:
    query = params.get("query", "")
    max_results = params.get("max_results", 3)
    return search(query, max_results)