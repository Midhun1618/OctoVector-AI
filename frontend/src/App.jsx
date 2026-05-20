import { useState, useRef } from "react";
import axios from "axios";
import "./App.css";
import logo from "./octovector_icon.png";

const API = "http://127.0.0.1:8000";

export default function App() {
  const [file, setFile] = useState(null);
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [status, setStatus] = useState("");
  const [loading, setLoading] = useState(false);
  const [copied, setCopied] = useState(false);
  const fileRef = useRef();

  const uploadPDF = async () => {
    if (!file) { alert("Select a PDF first."); return; }
    const formData = new FormData();
    formData.append("file", file);
    try {
      setLoading(true);
      setStatus("Indexing document…");
      const res = await axios.post(`${API}/upload`, formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setStatus(res.data.message || "Document ready.");
    } catch {
      setStatus("Upload failed.");
    } finally {
      setLoading(false);
    }
  };

  const askQuestion = async () => {
    if (!question.trim()) return;
    try {
      setLoading(true);
      setStatus("Thinking…");
      setAnswer("");
      const res = await axios.post(`${API}/query`, { question });
      setAnswer(res.data.answer);
      setStatus("");
    } catch {
      setStatus("Error generating answer.");
    } finally {
      setLoading(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    const f = e.dataTransfer.files[0];
    if (f?.type === "application/pdf") setFile(f);
  };

  const copyAnswer = () => {
    if (!answer) return;
    navigator.clipboard.writeText(answer);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="app">
      <header className="header">
        <div className="logo-wrap">
          <img
            src={logo}
            alt="OctoVector"
            onError={e => {
              e.target.style.display = "none";
              e.target.parentNode.innerHTML =
                '<span class="logo-fallback">OV</span>';
            }}
          />
        </div>
        <h1 className="header-title">OctoVector AI</h1>
        <p className="header-tagline">
          High-performance RAG · Dense + Sparse fusion · Cross-encoder reranking
        </p>
        <p className="header-tagline-error">
          The backend is currently unavailable due to memory limitations on the deployment platform. I'm actively working on resolving the issue.
        </p>
      </header>

      {status && (
        <div className="status-line">
          {loading && <span className="spin" />}
          {status}
        </div>
      )}

      <section className="block">
        <p className="block-label">Document</p>
        <div
          className="drop-zone"
          onClick={() => fileRef.current.click()}
          onDragOver={e => e.preventDefault()}
          onDrop={handleDrop}
        >
          <input
            ref={fileRef}
            type="file"
            className="file-input"
            accept=".pdf"
            onChange={e => setFile(e.target.files[0])}
          />
          <span className="drop-icon">⎗</span>
          <p className="drop-text">
            <span>Choose a file</span> or drag it here
          </p>
          <p className="drop-sub">PDF · up to 50 MB</p>
          {file && (
            <span className="file-tag">
              ✓ {file.name.length > 40 ? file.name.slice(0, 37) + "…" : file.name}
            </span>
          )}
        </div>
        <div className="btn-row">
          <button className="btn-main" onClick={uploadPDF} disabled={loading}>
            Process document
          </button>
          <button
            className="btn-sec"
            onClick={() => { setFile(null); if (fileRef.current) fileRef.current.value = ""; }}
          >
            Clear
          </button>
        </div>
      </section>

      <hr className="divider" />

      <section className="block">
        <p className="block-label">Question</p>
        <textarea
          className="q-input"
          placeholder="What would you like to know?"
          value={question}
          maxLength={2000}
          onChange={e => setQuestion(e.target.value)}
          onKeyDown={e => {
            if ((e.ctrlKey || e.metaKey) && e.key === "Enter") askQuestion();
          }}
        />
        <div className="q-meta">
          <span>ctrl + enter to send</span>
          <span>{question.length} / 2000</span>
        </div>
        <button className="btn-ask" onClick={askQuestion} disabled={loading}>
          Generate answer
        </button>
      </section>

      <section className="block">
        <p className="block-label">Answer</p>
        <div className="answer-box">
          <div className="answer-head">
            <div className="answer-head-label">
              <span className="answer-dot" />
              Result
            </div>
            <button className="copy-btn" onClick={copyAnswer}>
              {copied ? "Copied" : "Copy"}
            </button>
          </div>
          <div className="answer-body">
            {answer || (
              <span className="answer-empty">
                Your answer will appear here.
              </span>
            )}
          </div>
        </div>
      </section>

    </div>
  );
}