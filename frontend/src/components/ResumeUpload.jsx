import { useState, useRef } from "react";
import { api } from "../api";
import { UploadIcon, FileIcon } from "./Icons";

export default function ResumeUpload({ onUploaded }) {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [dragActive, setDragActive] = useState(false);
  const inputRef = useRef(null);

  const handleFile = (f) => {
    if (!f) return;
    setFile(f);
    setError("");
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setDragActive(false);
    handleFile(e.dataTransfer.files?.[0]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) return;
    setLoading(true);
    setError("");
    try {
      const resume = await api.uploadResume(file);
      onUploaded(resume);
    } catch (err) {
      setError("Upload failed. Please try a PDF or DOCX resume.");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <form className="card upload-card" onSubmit={handleSubmit}>
      <div className="section-title"><UploadIcon /><h2>Upload your resume</h2></div>
      <p className="muted small">PDF or DOCX. We'll extract your skills and score it against ATS heuristics.</p>

      <label
        className={dragActive ? "dropzone active" : "dropzone"}
        onDragOver={(e) => { e.preventDefault(); setDragActive(true); }}
        onDragLeave={() => setDragActive(false)}
        onDrop={handleDrop}
      >
        <input
          ref={inputRef}
          type="file"
          accept=".pdf,.docx"
          onChange={(e) => handleFile(e.target.files[0])}
        />
        <div className="dropzone-icon"><UploadIcon /></div>
        <strong>{dragActive ? "Drop it here" : "Drag & drop your resume"}</strong>
        <span className="muted small">or click to browse</span>
        {file && (
          <div className="file-chip"><FileIcon /> {file.name}</div>
        )}
      </label>

      <button type="submit" disabled={!file || loading} style={{ marginTop: 16 }}>
        {loading ? "Analyzing..." : "Analyze Resume"}
      </button>
      {error && <p className="error">{error}</p>}
    </form>
  );
}
