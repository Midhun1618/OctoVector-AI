import { useState } from "react";
import axios from "axios";

export default function App() {

  const [file, setFile] = useState(null);
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [status, setStatus] = useState("");

  const API = import.meta.env.VITE_API_URL;

  const uploadPDF = async () => {

    if (!file) {
      alert("Please select a PDF.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {

      setStatus("Uploading and processing PDF...");

      const response = await axios.post(
        `${API}/upload`,
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );

      setStatus(response.data.message);

    } catch (err) {

      console.error(err);
      setStatus("Upload failed.");

    }
  };

  const askQuestion = async () => {

    if (!question.trim()) return;

    try {

      setStatus("Generating answer...");

      const response = await axios.post(
        `${API}/query`,
        {
          question,
        }
      );

      setAnswer(response.data.answer);

      setStatus("");

    } catch (err) {

      console.error(err);
      setStatus("Error generating answer.");

    }
  };

  return (
    <div className="container">

      <h1 className="title">
        OctoVector AI
      </h1>

      <p className="subtitle">
        Upload PDF and ask questions using RAG
      </p>

      <div className="chat-box">

        <input
          type="file"
          accept=".pdf"
          onChange={(e) => setFile(e.target.files[0])}
        />

        <button onClick={uploadPDF}>
          Upload PDF
        </button>

        <br /><br />

        <input
          type="text"
          placeholder="Ask a question..."
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
        />

        <br /><br />

        <button onClick={askQuestion}>
          Ask
        </button>

        <div style={{ marginTop: "20px" }}>
          {status}
        </div>

        <div style={{ marginTop: "30px" }}>
          <strong>Answer:</strong>

          <p style={{
            marginTop: "10px",
            lineHeight: "1.8",
            whiteSpace: "pre-wrap",
          }}>
            {answer}
          </p>

        </div>

      </div>

    </div>
  );
}