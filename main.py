from __future__ import annotations

import os
import logging

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

from pipelines.ingestion_pipeline import process_pdf
from embedding.embedder import embed_chunks
from pipelines.retrieval_pipeline import retrieve_chunks
from pipelines.generation_pipeline import generate_response


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s — %(message)s",
    datefmt="%H:%M:%S",
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

stored_chunks = None
stored_embeddings = None

@app.get("/")
def home():
    return {
        "message": "OctoVector Backend Running"
    }

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):

    global stored_chunks
    global stored_embeddings

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    # SAVE PDF
    with open(file_path, "wb") as f:
        f.write(await file.read())

    print("\n============================================================")
    print(" PDF INGESTION STARTED ")
    print("============================================================")

    chunks = process_pdf(file_path)

    print(f"\nChunks created: {len(chunks)}")

    embeddings = embed_chunks(chunks)

    print(f"Embedding shape: {embeddings.shape}")

    stored_chunks = chunks
    stored_embeddings = embeddings

    return {
        "message": "PDF uploaded and processed successfully.",
        "chunks": len(chunks),
    }


@app.post("/query")
def query(data: dict):

    global stored_chunks
    global stored_embeddings

    if stored_chunks is None:
        return {
            "answer": "Please upload a PDF first."
        }

    question = data.get("question", "").strip()

    if not question:
        return {
            "answer": "Question cannot be empty."
        }

    print("\n============================================================")
    print(" QUERY RECEIVED ")
    print("============================================================")

    print(f"\nQuestion: {question}")

    retrieved = retrieve_chunks(
        query=question,
        chunks=stored_chunks,
        embeddings=stored_embeddings,
        top_k=5,
    )

    print(f"\nRetrieved {len(retrieved)} chunks")

    result = generate_response(
        query=question,
        retrieved_chunks=retrieved,
    )

    answer = result["answer"]

    return {
        "answer": answer
    }