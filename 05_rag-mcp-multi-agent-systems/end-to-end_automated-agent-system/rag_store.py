# RAG Backend
# Retrieval Layer

import numpy as np

# This file holds a small list of documents and provides 3 Core functions

DOCS = [
    "Automated agent can fetch external data for monitoring.",
    "RAG retrieves relevant documents by comparing text similarity to the query.",
    "Multi-agent workflows let each role specialize in a specific step of the pipeline."
]

## Converts Text into a Numeric Vector by converting characters to their ASCII values
def embed(text: str):
    v = [float(ord(c)) for c in text[:64]]
    v += [0.0] * (64 - len(v))
    return np.array(v)

## Measures the Similarity between 2 Vectors
def cosine(a, b):
    return float((a @ b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-8))

## Takes a User Query, Embeds it, Compares it to the DOCS above in 'rag_store.py' using Cosine Similarity, and Returns the two most relevant ones
def retrieve_rag(query: str):
    qv = embed(query)
    scored = [(cosine(qv, embed(doc)), doc) for doc in DOCS]
    scored.sort(reverse = True)
    return [doc for _, doc in scored[:2]]

# ^This all gives our Agent basic Retrieval capability without needing a real Vector Database