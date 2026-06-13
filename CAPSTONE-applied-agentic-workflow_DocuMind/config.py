# Central Configuration - every other File imports from here

import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")
if not API_KEY:
    raise RuntimeError("Missing OPENAI_API_KEY in .env")

client = OpenAI(api_key = API_KEY)

# Model for Chat Completions
LLM_MODEL = "gpt-4o-mini"

# Model for (Real) Embeddings
EMBEDDING_MODEL = "text-embedding-3-small"

# RAG Settings
CHROMA_COLLECTION = "document"
TOP_K_RESULTS = 3

# Agent Settings
MAX_RETRIES = 2
CRITIC_THRESHOLD = 0.7