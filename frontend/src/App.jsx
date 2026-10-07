import { useState } from "react";
import "./App.css";

const API_URL = import.meta.env.VITE_API_URL;

function App() {
  const [file, setFile] = useState(null);
  const [uploadStatus, setUploadStatus] = useState("");
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleFileChange = (event) => {
    const selectedFile = event.target.files[0];

    if (selectedFile && selectedFile.type !== "application/pdf") {
      setUploadStatus("Please select a PDF file.");
      setFile(null);
      return;
    }

    setFile(selectedFile);
    setUploadStatus("");
  };

  const uploadPDF = async () => {
    if (!file) {
      setUploadStatus("Please select a PDF first.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      setUploadStatus("Uploading PDF...");

      const response = await fetch(`${API_URL}/upload`, {
        method: "POST",
        body: formData,
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error("Upload failed");
      }

      setUploadStatus(
        `✓ PDF uploaded successfully. ${data.number_of_pages} pages and ${data.number_of_chunks} chunks created.`
      );
    } catch (error) {
      console.error(error);
      setUploadStatus("✗ Could not upload the PDF.");
    }
  };

  const askQuestion = async () => {
    if (!question.trim()) {
      return;
    }

    const userQuestion = question.trim();

    setMessages((previous) => [
      ...previous,
      {
        role: "user",
        content: userQuestion,
      },
    ]);

    setQuestion("");
    setLoading(true);

    try {
      const response = await fetch(`${API_URL}/chat`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          question: userQuestion,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error("Failed to get answer");
      }

      setMessages((previous) => [
        ...previous,
     {
      role: "assistant",
      content: data.answer,
      sources: data.sources || [],
     },
     ]);
    } catch (error) {
      console.error(error);

      setMessages((previous) => [
        ...previous,
        {
          role: "assistant",
          content: "Sorry, I couldn't get an answer from the server.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const clearChat = () => {
    setMessages([]);
  };

  return (
    <div className="app">

      <header className="header">
        <div>
          <h1>📚 RAG PDF Chatbot</h1>
          <p>
            Upload a document and ask questions using AI-powered retrieval.
          </p>
        </div>
      </header>

      <main className="container">

        {/* Upload Section */}
        <section className="upload-section">

          <div className="section-header">
            <div>
              <h2>Upload Document</h2>
              <p>Select a PDF to start chatting with your document.</p>
            </div>
          </div>

          <div className="upload-box">

            <div className="upload-icon">
              📄
            </div>

            <input
              id="pdf-upload"
              type="file"
              accept=".pdf"
              onChange={handleFileChange}
            />

            {file && (
              <div className="selected-file">
                <span>📄</span>
                <span>{file.name}</span>
              </div>
            )}

            <button
              className="upload-button"
              onClick={uploadPDF}
            >
              Upload PDF
            </button>

            {uploadStatus && (
              <p className="status">
                {uploadStatus}
              </p>
            )}

          </div>

        </section>

        {/* Chat Section */}
        <section className="chat-section">

          <div className="chat-header">

            <div>
              <h2>💬 Chat with your PDF</h2>
              <p>Ask questions based on the uploaded document.</p>
            </div>

            {messages.length > 0 && (
              <button
                className="clear-button"
                onClick={clearChat}
              >
                Clear Chat
              </button>
            )}

          </div>

          <div className="chat-box">

            {messages.length === 0 && (
              <div className="empty-chat">

                <div className="empty-icon">
                  🤖
                </div>

                <h3>Start a conversation</h3>

                <p>
                  Upload a PDF and ask a question about its content.
                </p>

              </div>
            )}

            {messages.map((message, index) => (

              <div
                key={index}
                className={`message ${message.role}`}
              >

                <div className="message-label">
                  {message.role === "user" ? "You" : "AI Assistant"}
                </div>

                <div className="message-content">
                  {message.content}
                </div>

                {message.role === "assistant" &&
                  message.sources &&
                  message.sources.length > 0 && (
                <div className="sources">

      <div className="sources-title">
        📚 Sources
      </div>

      <div className="source-list">

        {message.sources.map((source, sourceIndex) => (
          <span
            className="source-item"
            key={sourceIndex}
          >
            📄 Page {source.page}
          </span>
        ))}

      </div>

    </div>
)}

              </div>

            ))}

            {loading && (
              <div className="message assistant">

                <div className="message-label">
                  AI Assistant
                </div>

                <div className="loading">
                  <span></span>
                  <span></span>
                  <span></span>
                  Thinking...
                </div>

              </div>
            )}

          </div>

          <div className="question-box">

            <input
              type="text"
              placeholder="Ask something about your PDF..."
              value={question}
              onChange={(event) => setQuestion(event.target.value)}
              onKeyDown={(event) => {
                if (event.key === "Enter") {
                  askQuestion();
                }
              }}
            />

            <button
              className="ask-button"
              onClick={askQuestion}
              disabled={loading}
            >
              {loading ? "Thinking..." : "Ask"}
            </button>

          </div>

        </section>

      </main>

      <footer>
        <p>
          RAG PDF Chatbot • FastAPI • LangChain • FAISS • Gemini
        </p>
      </footer>

    </div>
  );
}

export default App;