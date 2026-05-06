import streamlit as st
import os

from pipelines.ingestion_pipeline import process_pdf
from embedding.embedder import embed_chunks
from indexing.index_manager import IndexManager
from retrieval.hybrid_retrieval import HybridRetriever
from reranking.cross_encoder import CrossEncoderReranker
from generation.prompt_builder import build_prompt
from generation.llm_client import generate_answer

st.set_page_config(page_title="RAG PDF QA", layout="wide")

st.title("📄 RAG PDF Question Answering")
st.write("Upload a PDF and ask questions about it")

# -----------------------
# File Upload
# -----------------------
uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

if uploaded_file:
    file_path = os.path.join("data/raw_pdfs", uploaded_file.name)

    with open(file_path, "wb") as f:
        f.write(uploaded_file.read())

    st.success("PDF uploaded successfully!")

    # -----------------------
    # Build Pipeline (once)
    # -----------------------
    if "index_manager" not in st.session_state:
        with st.spinner("Processing PDF..."):
            chunks = process_pdf(file_path)
            embeddings = embed_chunks(chunks)

            index_manager = IndexManager()
            index_manager.build_index(chunks, embeddings)

            st.session_state.chunks = chunks
            st.session_state.index_manager = index_manager

        st.success("PDF processed!")

# -----------------------
# Query Input
# -----------------------
query = st.text_input("Ask a question")

if query and "index_manager" in st.session_state:
    with st.spinner("Thinking..."):

        # Retrieval
        retriever = HybridRetriever(
            st.session_state.index_manager,
            st.session_state.chunks
        )
        retrieved = retriever.retrieve(query, k=5)

        # Reranking
        reranker = CrossEncoderReranker()
        final_chunks = reranker.rerank(query, retrieved, top_k=3)

        # Prompt + LLM
        prompt = build_prompt(query, final_chunks)
        answer = generate_answer(prompt)

    # -----------------------
    # Output
    # -----------------------
    st.subheader("💡 Answer")
    st.write(answer)

    # -----------------------
    # Debug View
    # -----------------------
    with st.expander("🔍 Retrieved Context"):
        for i, chunk in enumerate(final_chunks):
            st.markdown(f"**Chunk {i+1} (Page {chunk['page']})**")
            st.write(chunk["text"][:500])
            st.markdown("---")