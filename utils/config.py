import os

CHUNK_SIZE: int    = int(os.getenv("CHUNK_SIZE",    800))
CHUNK_OVERLAP: int = int(os.getenv("CHUNK_OVERLAP", 150))

DENSE_TOP_K: int   = int(os.getenv("DENSE_TOP_K",  30))
SPARSE_TOP_K: int  = int(os.getenv("SPARSE_TOP_K", 30))
RERANK_TOP_K: int  = int(os.getenv("RERANK_TOP_K", 10))
FINAL_TOP_K: int   = int(os.getenv("FINAL_TOP_K",   5))

EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
RERANK_MODEL: str    = os.getenv("RERANK_MODEL",    "cross-encoder/ms-marco-MiniLM-L-6-v2")

VECTOR_DB: str = os.getenv("VECTOR_DB", "faiss")

GEMINI_API_KEY: str  = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL: str    = os.getenv("GEMINI_MODEL",   "gemini-2.0-flash")
GEMINI_BASE_URL: str = "https://generativelanguage.googleapis.com/v1beta/models"

RRF_K: int = int(os.getenv("RRF_K", 60))