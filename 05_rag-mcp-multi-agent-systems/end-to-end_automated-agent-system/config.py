# Core Configuration for our Agent System - Central Setup Point that the rest of the System relies on

import os
from dotenv import load_dotenv
from openai import OpenAI

# Install Dependencies
# pip install openai python-dotenv numpy requests imapclient pyzmail36 google-api-python-client google-auth-oauthlib google-auth-httplib2

load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")
if not API_KEY:
    raise RuntimeError("Missing OPENAI_API_KEY in .env")

client = OpenAI(api_key=API_KEY)
MODEL_NAME = "gpt-4o-mini"  # Swap to "gpt-4o" if you want the full model
