import { useState, useRef } from "react";
import axios from "axios";

const API = import.meta.env.VITE_API_URL;

export default function App() {
  const [file, setFile] = useState(null);
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [status, setStatus] = useState("");
  const [loading, setLoading] = useState(false);
  const [dragging, setDragging] = useState(false);
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
      setStatus("Retrieving answer…");
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
    setDragging(false);
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
    <>
      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=IBM+Plex+Mono:wght@300;400;500&display=swap');

        *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

        body {
          background: #f5f0e8;
          font-family: 'IBM Plex Mono', monospace;
          color: #0f0d0b;
          min-height: 100vh;
        }

        .app {
          max-width: 780px;
          margin: 0 auto;
          padding: 0 0 80px;
          background: #f5f0e8;
          position: relative;
        }

        /* ── TOP BAR ── */
        .topbar {
          display: flex;
          align-items: center;
          justify-content: space-between;
          padding: 18px 32px 16px;
          border-bottom: 1px solid rgba(0,0,0,0.1);
        }

        .brand {
          display: flex;
          align-items: center;
          gap: 12px;
        }

        .logo-hex {
          width: 36px; height: 36px;
          background: #1a0040;
          clip-path: polygon(50% 0%,93% 25%,93% 75%,50% 100%,7% 75%,7% 25%);
          display: flex; align-items: center; justify-content: center;
          flex-shrink: 0;
        }

        .logo-hex img {
          width: 22px; height: 22px;
          object-fit: contain;
          filter: brightness(0) invert(1);
        }

        .brand-text .name {
          font-family: 'Instrument Serif', serif;
          font-size: 18px;
          color: #0f0d0b;
          line-height: 1;
        }

        .brand-text .sub {
          font-size: 9px;
          letter-spacing: 0.15em;
          text-transform: uppercase;
          color: #7a7268;
          margin-top: 2px;
        }

        .status-pill {
          font-size: 10px;
          letter-spacing: 0.1em;
          text-transform: uppercase;
          color: #6b21ff;
          background: #ede5ff;
          border: 1px solid #c4a7ff;
          padding: 4px 12px;
          border-radius: 2px;
          display: flex; align-items: center; gap: 6px;
          min-height: 28px;
          transition: opacity 0.3s;
          opacity: ${status ? 1 : 0};
        }

        .spin-dot {
          width: 6px; height: 6px;
          border: 1.5px solid rgba(107,33,255,0.3);
          border-top-color: #6b21ff;
          border-radius: 50%;
          animation: sp 0.7s linear infinite;
        }

        @keyframes sp { to { transform: rotate(360deg); } }

        /* ── SECTION HEADERS ── */
        .sec-row {
          display: flex;
          align-items: baseline;
          gap: 10px;
          padding: 24px 32px 12px;
          border-bottom: 1px solid rgba(0,0,0,0.07);
        }

        .sec-num {
          font-size: 9px;
          letter-spacing: 0.2em;
          text-transform: uppercase;
          color: #6b21ff;
        }

        .sec-label {
          font-family: 'Instrument Serif', serif;
          font-style: italic;
          font-size: 16px;
          color: #3a3530;
        }

        /* ── DROP ZONE ── */
        .drop-zone {
          margin: 20px 32px 0;
          border: 1.5px dashed ${dragging ? "#a07aff" : "rgba(0,0,0,0.15)"};
          background: ${dragging ? "#ede5ff" : "#ede8de"};
          border-radius: 4px;
          padding: 28px 20px;
          text-align: center;
          cursor: pointer;
          transition: border-color 0.2s, background 0.2s;
        }

        .drop-zone:hover {
          border-color: #a07aff;
          background: #ede5ff;
        }

        .pdf-badge {
          display: inline-flex;
          align-items: center;
          justify-content: center;
          width: 36px; height: 44px;
          border: 1.5px solid rgba(0,0,0,0.15);
          border-radius: 3px;
          font-size: 9px;
          letter-spacing: 0.1em;
          text-transform: uppercase;
          color: #7a7268;
          background: #f5f0e8;
          margin-bottom: 10px;
          position: relative;
        }

        .pdf-badge::after {
          content: '';
          position: absolute;
          top: -1px; right: -1px;
          width: 8px; height: 8px;
          background: #ede8de;
          border-left: 1.5px solid rgba(0,0,0,0.15);
          border-bottom: 1.5px solid rgba(0,0,0,0.15);
        }

        .drop-text {
          font-size: 11px;
          color: #7a7268;
          line-height: 1.7;
          letter-spacing: 0.03em;
        }

        .drop-text strong { color: #6b21ff; font-weight: 500; }

        .file-chosen {
          display: inline-flex; align-items: center; gap: 6px;
          margin-top: 10px;
          font-size: 10px;
          letter-spacing: 0.05em;
          color: #6b21ff;
          background: rgba(107,33,255,0.08);
          border: 1px solid rgba(107,33,255,0.25);
          padding: 4px 10px;
          border-radius: 2px;
        }

        /* ── ACTION ROW ── */
        .act-row {
          display: flex;
          gap: 8px;
          padding: 14px 32px 0;
        }

        .btn-primary {
          flex: 1;
          font-family: 'IBM Plex Mono', monospace;
          font-size: 11px;
          font-weight: 500;
          letter-spacing: 0.12em;
          text-transform: uppercase;
          background: #1a0040;
          color: #e8d8ff;
          border: none;
          padding: 12px 20px;
          border-radius: 2px;
          cursor: pointer;
          transition: background 0.2s;
          display: flex; align-items: center; justify-content: center; gap: 8px;
        }

        .btn-primary:hover { background: #2d0070; }
        .btn-primary:disabled { opacity: 0.35; cursor: not-allowed; }

        .btn-ghost {
          font-family: 'IBM Plex Mono', monospace;
          font-size: 11px;
          letter-spacing: 0.1em;
          text-transform: uppercase;
          background: transparent;
          color: #7a7268;
          border: 1px solid rgba(0,0,0,0.12);
          padding: 12px 16px;
          border-radius: 2px;
          cursor: pointer;
          transition: border-color 0.2s, color 0.2s;
        }

        .btn-ghost:hover { border-color: #7a7268; color: #0f0d0b; }

        /* ── QUESTION ── */
        .q-wrap {
          padding: 20px 32px 0;
        }

        .q-label {
          font-size: 9px;
          letter-spacing: 0.15em;
          text-transform: uppercase;
          color: #7a7268;
          margin-bottom: 10px;
        }

        .q-input {
          width: 100%;
          min-height: 110px;
          resize: vertical;
          background: transparent;
          border: none;
          border-bottom: 1.5px solid rgba(0,0,0,0.12);
          font-family: 'Instrument Serif', serif;
          font-style: italic;
          font-size: 18px;
          color: #0f0d0b;
          line-height: 1.6;
          outline: none;
          padding: 4px 0 12px;
          transition: border-color 0.2s;
          caret-color: #6b21ff;
        }

        .q-input::placeholder { color: rgba(0,0,0,0.2); }
        .q-input:focus { border-bottom-color: #6b21ff; }

        .q-meta {
          display: flex;
          justify-content: space-between;
          align-items: center;
          padding: 8px 0 0;
        }

        .q-hint {
          font-size: 9px;
          letter-spacing: 0.08em;
          color: rgba(0,0,0,0.25);
        }

        .q-count {
          font-size: 9px;
          letter-spacing: 0.08em;
          color: rgba(0,0,0,0.25);
        }

        .btn-ask {
          width: calc(100% - 64px);
          margin: 16px 32px 0;
          font-family: 'IBM Plex Mono', monospace;
          font-size: 11px;
          font-weight: 500;
          letter-spacing: 0.14em;
          text-transform: uppercase;
          background: #6b21ff;
          color: #fff;
          border: none;
          padding: 13px;
          border-radius: 2px;
          cursor: pointer;
          transition: background 0.2s;
          display: flex; align-items: center; justify-content: center; gap: 10px;
        }

        .btn-ask:hover { background: #5510e0; }
        .btn-ask:disabled { opacity: 0.35; cursor: not-allowed; }

        /* ── ANSWER ── */
        .ans-section {
          margin: 32px 32px 0;
          border: 1px solid rgba(0,0,0,0.1);
          border-radius: 4px;
          overflow: hidden;
          background: #ede8de;
        }

        .ans-head {
          display: flex;
          align-items: center;
          justify-content: space-between;
          padding: 12px 18px;
          border-bottom: 1px solid rgba(0,0,0,0.08);
          background: #e2dbd0;
        }

        .ans-tag {
          display: flex; align-items: center; gap: 8px;
          font-size: 9px;
          letter-spacing: 0.15em;
          text-transform: uppercase;
          color: #7a7268;
        }

        .ans-diamond {
          width: 7px; height: 7px;
          background: #6b21ff;
          transform: rotate(45deg);
          border-radius: 1px;
          flex-shrink: 0;
        }

        .copy-btn {
          font-family: 'IBM Plex Mono', monospace;
          font-size: 9px;
          letter-spacing: 0.1em;
          text-transform: uppercase;
          background: none;
          color: #7a7268;
          border: 1px solid rgba(0,0,0,0.12);
          padding: 3px 8px;
          border-radius: 2px;
          cursor: pointer;
          transition: all 0.2s;
        }

        .copy-btn:hover { border-color: #7a7268; color: #0f0d0b; }

        .ans-body {
          padding: 22px 24px 28px;
          font-family: 'Instrument Serif', serif;
          font-size: 18px;
          line-height: 1.75;
          color: #0f0d0b;
          min-height: 100px;
          white-space: pre-wrap;
        }

        .ans-placeholder {
          font-family: 'IBM Plex Mono', monospace;
          font-size: 11px;
          letter-spacing: 0.04em;
          color: rgba(0,0,0,0.2);
          font-style: normal;
        }

        .ans-placeholder::before {
          content: '— ';
          color: #6b21ff;
          opacity: 0.5;
        }
      `}</style>

      <div className="app">

        {/* Top bar */}
        <div className="topbar">
          <div className="brand">
            
            <div className="brand-text">
                <div className="logo-hex">
              <img src="/octovector_icon.png" alt="OctoVector"
                onError={e => { e.target.style.display = 'none'; e.target.parentNode.innerHTML = '<span style="font-size:11px;color:#e8d8ff;font-family:monospace">OV</span>'; }}
              />
            </div>
              <div className="name">OctoVector</div>
              <div className="sub">Hybrid RAG · v2</div>
            </div>
          </div>
          <div className="status-pill" style={{ opacity: status ? 1 : 0 }}>
            {loading && <div className="spin-dot" />}
            {status}
          </div>
        </div>

        {/* Upload section */}
        <div className="sec-row">
          <span className="sec-num">01</span>
          <span className="sec-label">Document ingestion</span>
        </div>

        <div
          className="drop-zone"
          onClick={() => fileRef.current.click()}
          onDragOver={e => { e.preventDefault(); setDragging(true); }}
          onDragLeave={() => setDragging(false)}
          onDrop={handleDrop}
        >
          <input
            ref={fileRef}
            type="file"
            accept=".pdf"
            style={{ display: "none" }}
            onChange={e => setFile(e.target.files[0])}
          />
          <div className="pdf-badge">PDF</div>
          <div className="drop-text">
            <strong>Drop a file here</strong> or click to browse<br />
            <span style={{ fontSize: "10px" }}>Portable Document Format · max 50 MB</span>
          </div>
          {file && (
            <div className="file-chosen">
              ⎘ {file.name.length > 36 ? file.name.slice(0, 33) + "…" : file.name}
            </div>
          )}
        </div>

        <div className="act-row">
          <button className="btn-primary" onClick={uploadPDF} disabled={loading}>
            ↑ Process document
          </button>
          <button className="btn-ghost" onClick={() => { setFile(null); if (fileRef.current) fileRef.current.value = ""; }}>
            Clear
          </button>
        </div>

        {/* Query section */}
        <div className="sec-row" style={{ marginTop: "28px" }}>
          <span className="sec-num">02</span>
          <span className="sec-label">Ask anything</span>
        </div>

        <div className="q-wrap">
          <div className="q-label">Your question</div>
          <textarea
            className="q-input"
            placeholder="What does the document say about…"
            value={question}
            maxLength={2000}
            onChange={e => setQuestion(e.target.value)}
            onKeyDown={e => { if ((e.ctrlKey || e.metaKey) && e.key === "Enter") askQuestion(); }}
          />
          <div className="q-meta">
            <span className="q-hint">ctrl + enter to submit</span>
            <span className="q-count">{question.length} / 2000</span>
          </div>
        </div>

        <button className="btn-ask" onClick={askQuestion} disabled={loading}>
          ⚡ Generate answer
        </button>

        {/* Answer */}
        <div className="ans-section">
          <div className="ans-head">
            <div className="ans-tag">
              <div className="ans-diamond" />
              Retrieved answer
            </div>
            <button className="copy-btn" onClick={copyAnswer}>
              {copied ? "Copied" : "Copy"}
            </button>
          </div>
          <div className="ans-body">
            {answer || (
              <span className="ans-placeholder">
                Upload a document and ask a question to see answers here.
              </span>
            )}
          </div>
        </div>

      </div>
    </>
  );
}