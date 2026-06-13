# Real RAG pipeline — OpenAI Embeddings + ChromaDB Vector Database

import chromadb
import pypdf
import os
from config import client, EMBEDDING_MODEL, CHROMA_COLLECTION, TOP_K_RESULTS

# Initialize ChromaDB (runs locally, no server needed)
chroma_client = chromadb.PersistentClient(path = "./chroma_db")
collection = chroma_client.get_or_create_collection(name = CHROMA_COLLECTION)


# Embedding
def embed_text(text: str) -> list[float]:
    response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=text
    )
    return response.data[0].embedding


# Document Ingestion
# The Ingestion functions Split Documents into Chunks (one page per Chunk for PDFs, 500 characters per Chunk for .txt files),
# Embed each Chunk, and Store it with Metadata
def ingest_pdf(filepath: str):
    print(f"Ingesting: {filepath}")
    reader = pypdf.PdfReader(filepath)

    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        if not text or len(text.strip()) < 30:
            continue

        # Each Page becomes one Chunk
        chunk_id = f"{os.path.basename(filepath)}_page_{i+1}"
        embedding = embed_text(text)

        collection.add(
            ids = [chunk_id],
            embeddings = [embedding],
            documents = [text],
            metadatas = [{"source": filepath, "page": i + 1}]
        )
        print(f"  ✓ Indexed page {i+1}")

    print(f"Done. {len(reader.pages)} pages ingested.\n")


def ingest_txt(filepath: str):
    print(f"Ingesting: {filepath}")
    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()

    # Split into ~500 Character Chunks
    chunks = [text[i:i+500] for i in range(0, len(text), 500)]

    for i, chunk in enumerate(chunks):
        if len(chunk.strip()) < 30:
            continue
        chunk_id = f"{os.path.basename(filepath)}_chunk_{i+1}"
        embedding = embed_text(chunk)

        collection.add(
            ids = [chunk_id],
            embeddings = [embedding],
            documents = [chunk],
            metadatas = [{"source": filepath, "chunk": i + 1}]
        )
        print(f"  ✓ Indexed chunk {i+1}")

    print(f"Done. {len(chunks)} chunks ingested.\n")


def ingest_document(filepath: str):
    ext = os.path.splitext(filepath)[1].lower()
    if ext == ".pdf":
        ingest_pdf(filepath)
    elif ext == ".txt":
        ingest_txt(filepath)
    else:
        print(f"Unsupported file type: {ext}. Use PDF or TXT.")


# Retrieval
def retrieve(query: str) -> list[dict]:
    query_embedding = embed_text(query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=TOP_K_RESULTS
    )

    chunks = []
    for i in range(len(results["documents"][0])):
        chunks.append({
            "text": results["documents"][0][i],
            "source": results["metadatas"][0][i]["source"],
            "distance": results["distances"][0][i]
        })

    return chunks


# Utility
def clear_collection():
    chroma_client.delete_collection(CHROMA_COLLECTION)
    print("Vector store cleared.")