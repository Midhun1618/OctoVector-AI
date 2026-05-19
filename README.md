<img width="200" height="200" alt="octovector_icon" src="https://github.com/user-attachments/assets/fdffae95-c96b-4c90-b62d-8aba5bce7643" />

# OctoVector-AI

A production-style Retrieval-Augmented Generation (RAG) system built with **FastAPI + React**, designed for intelligent PDF understanding through advanced retrieval engineering.

Unlike simple "upload PDF → ask GPT" projects, OctoVector-AI implements a complete retrieval pipeline with:

- Dense Retrieval
- Sparse Retrieval
- Hybrid Search
- Reciprocal Rank Fusion (RRF)
- Cross Encoder Re-ranking
- Grounded Prompt Generation
- Hallucination Reduction

The system focuses on one principle:

> Better retrieval = better answers.

---

# Features

### Document Intelligence
- PDF text extraction
- Text cleaning and normalization
- Semantic chunking
- Sentence-aware segmentation

### Embedding Pipeline
- SentenceTransformer embeddings
- Precomputed embedding storage
- Efficient lifecycle management

### Retrieval System
- Dense retrieval using FAISS
- Sparse retrieval using BM25
- Hybrid retrieval pipeline
- Reciprocal Rank Fusion (RRF)

### Ranking Layer
- Cross Encoder reranking
- Heuristic relevance boosting
- Precision-focused retrieval optimization

### Generation Layer
- Gemini-powered response generation
- Grounded prompt construction
- Context injection
- Hallucination reduction

### Backend Engineering
- FastAPI architecture
- Async APIs
- CORS support
- Logging
- Persistent upload storage

### Frontend Integration
- React upload interface
- Question-answer workflow
- Real-time interaction

---

# System Architecture

```text
                    ┌─────────────────────────┐
                    │     React Frontend      │
                    │ Upload + Ask Questions  │
                    └────────────┬────────────┘
                                 │
                                 ▼
                    ┌─────────────────────────┐
                    │     FastAPI Backend     │
                    └────────────┬────────────┘
                                 │
         ┌───────────────────────┴──────────────────────┐
         │                                              │
         ▼                                              ▼

 ┌──────────────────┐                         ┌──────────────────┐
 │   /upload API    │                         │    /query API    │
 └────────┬─────────┘                         └────────┬─────────┘
          │                                            │
          ▼                                            ▼

 ┌──────────────────┐                     ┌──────────────────────┐
 │ PDF Ingestion    │                     │ Query Processing     │
 │ Cleaning         │                     │ Hybrid Retrieval     │
 │ Chunking         │                     │ Reranking            │
 └────────┬─────────┘                     └────────┬─────────────┘
          │                                         │
          ▼                                         ▼

 ┌──────────────────┐                     ┌──────────────────────┐
 │ Embedding Model  │                     │ Context Selection    │
 │ SentenceTransform│                     └────────┬─────────────┘
 └────────┬─────────┘                              │
          ▼                                        ▼

 ┌──────────────────┐                     ┌──────────────────────┐
 │ FAISS Vector DB  │                     │ Prompt Construction  │
 └────────┬─────────┘                     └────────┬─────────────┘
          │                                        │
          ▼                                        ▼

 ┌──────────────────┐                     ┌──────────────────────┐
 │ Stored Embeddings│                     │ Gemini Generation    │
 └──────────────────┘                     └────────┬─────────────┘
                                                   ▼
                                        ┌──────────────────────┐
                                        │ Grounded Response    │
                                        └──────────────────────┘
```

---

# API Structure

## Upload Endpoint

```http
POST /upload
```

Handles:

- PDF upload
- Text extraction
- Cleaning
- Semantic chunking
- Embedding generation
- Vector preparation

---

## Query Endpoint

```http
POST /query
```

Handles:

- Hybrid retrieval
- Reranking
- Context selection
- Prompt construction
- Gemini generation
- Answer delivery

---

# Upload Workflow

```text
PDF Upload
    ↓
Disk Persistence
    ↓
Text Extraction
    ↓
Cleaning
    ↓
Chunking
    ↓
Embedding Generation
    ↓
Store Chunks + Embeddings
```

---

# Retrieval Workflow

```text
User Question
      ↓
retrieve_chunks()
      ↓
Hybrid Retrieval
      ↓
RRF Fusion
      ↓
Cross Encoder Reranking
      ↓
generate_response()
      ↓
Gemini Answer
```

---

# Core Architecture Layers

## 1. Document Intelligence Layer

Responsible for:

- PDF extraction
- Normalization
- Semantic chunking

---

## 2. Retrieval Layer

Responsible for:

- Dense retrieval
- Sparse retrieval
- FAISS search
- BM25 search

---

## 3. Ranking Layer

Responsible for:

- RRF Fusion
- Cross Encoder reranking
- Heuristic boosting

---

## 4. Grounding Layer

Responsible for:

- Prompt construction
- Citation-aware context injection
- Hallucination reduction

---

## 5. Generation Layer

Responsible for:

- Gemini interaction
- Response synthesis

---

## 6. Application Layer

Responsible for:

- API orchestration
- Frontend integration
- Lifecycle management

---

# Technical Highlights

### Hybrid Retrieval

Combines:

- Semantic search
- Lexical search
- Retrieval fusion

Provides significantly better results than standalone retrieval approaches.

---

### Cross Encoder Precision Layer

Improves ranking quality after retrieval and increases answer relevance.

---

### Sentence-Aware Chunking

More context-preserving than fixed-size chunking.

---

### Reciprocal Rank Fusion (RRF)

Advanced retrieval engineering technique for combining ranking systems.

---

### Grounded Prompting

Reduces hallucinations and improves answer reliability.

---

# Tech Stack

## Backend

- FastAPI
- Python
- SentenceTransformers
- FAISS
- BM25
- Gemini API

## Frontend

- React

## AI / Retrieval

- Dense Retrieval
- Sparse Retrieval
- Hybrid Search
- Cross Encoder Reranking
- RRF Fusion

---

# Project Structure

```text
project/
│
├── frontend/
│   └── React UI
│
├── main.py
├── ingestion/
├── retrieval/
├── generation/
├── embeddings/
└── uploads/
│
├── vector_store/
│
└── README.md
```

---

# Design Philosophy

This system follows a retrieval-first architecture:

> The quality of generated answers depends primarily on retrieval quality.

Instead of relying solely on an LLM, the system prioritizes strong information retrieval before generation.

---

# Future Improvements

- Multi-document support
- Streaming responses
- Persistent vector database
- User authentication
- Conversation memory
- Citation highlighting
- Kubernetes deployment

---

# Skills Demonstrated

### NLP Engineering

- Semantic chunking
- Embeddings
- Text preprocessing

### Information Retrieval

- BM25
- FAISS
- Hybrid Retrieval
- RRF
- Reranking

### LLM Systems

- Prompt engineering
- Grounding
- Hallucination control

### Backend Engineering

- FastAPI
- Modular architecture
- Logging
- Persistence

### Frontend Engineering

- React integration
- Async workflows

Built with retrieval engineering at the core.

---

# About the Name: OctoVector AI

The name **OctoVector AI** combines two ideas that represent the system’s core architecture.

**Octo** is inspired by the **Octopus**, symbolizing intelligence, adaptability, and multiple components working together in parallel—similar to the system’s multi-stage pipeline involving retrieval, fusion, reranking, and generation.

**Vector** represents **embedding vectors**, the foundation of semantic search, enabling the system to understand meaning and context beyond simple keyword matching.

Together, **OctoVector AI** represents:

- **Parallel Intelligence** → multiple retrieval strategies working together  
- **Semantic Depth** → understanding meaning through embeddings  
- **Precision & Adaptability** → refining and retrieving the most relevant information  

The name reflects a system designed to intelligently navigate and refine knowledge across multiple layers to deliver accurate, context-aware answers.
