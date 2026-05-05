import streamlit as st
import time

# Import your pipeline functions
# You will implement these
from ingestion.pipeline import process_pdf
from retrieval.pipeline import retrieve_and_rerank
from generation.pipeline import generate_answer


st.set_page_config(page_title="PDF RAG Engine", layout="wide")

st.title("📄 PDF Intelligence Engine")
st.markdown("Ask questions from your documents with grounded answers.")

# -------------------------------
# Upload Section
# -------------------------------
st.header("Upload PDF")

uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file:
    with st.spinner("Processing PDF..."):
        process_pdf(uploaded_file)  # your ingestion pipeline
    st.success("PDF processed successfully!")

# -------------------------------
# Query Section
# -------------------------------
st.header("Ask a Question")

query = st.text_input("Enter your question")

if st.button("Ask"):
    if not query:
        st.warning("Please enter a question.")
    else:
        with st.spinner("Retrieving and generating answer..."):
            start_time = time.time()

            # Retrieval + reranking
            chunks = retrieve_and_rerank(query)

            # Generate answer
            answer = generate_answer(query, chunks)

            latency = round((time.time() - start_time) * 1000, 2)

        # -------------------------------
        # Display Answer
        # -------------------------------
        st.subheader("Answer")
        st.write(answer)

        # -------------------------------
        # Display Sources
        # -------------------------------
        st.subheader("Sources")

        if chunks:
            for i, chunk in enumerate(chunks):
                with st.expander(f"Chunk {i+1} (Page {chunk.get('page', 'N/A')})"):
                    st.write(chunk["text"])
        else:
            st.warning("No relevant context found.")

        # -------------------------------
        # Debug Info (Optional)
        # -------------------------------
        st.caption(f"Latency: {latency} ms")