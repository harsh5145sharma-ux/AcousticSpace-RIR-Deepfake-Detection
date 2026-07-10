import { useState } from "react";


function AudioUpload() {
  const [file, setFile] = useState(null);
  const handleUpload = () => {
  if (!file) {
    alert("Please select a file first.");
    return;
  }

  console.log("Uploading:", file);
  // Yahan baad me API call karenge
};
  return (
    <div
      style={{
        backgroundColor: "#ffffff",
        padding: "25px",
        borderRadius: "15px",
        boxShadow: "0 5px 15px rgba(0,0,0,0.1)",
      }}
    >
      <h2 style={{ color: "#2563EB" }}>Upload Audio</h2>

      <p style={{ color: "#555" }}>
        Select a WAV or MP3 file for AI analysis.
      </p>

      <input
        type="file"
        accept=".wav,.mp3"
        onChange={(e) => setFile(e.target.files[0])}
      />

      <br />
      <br />

      <button
        onClick={handleUpload}
        style={{
          backgroundColor: "#2563EB",
          color: "white",
          border: "none",
          padding: "12px 25px",
          borderRadius: "8px",
          cursor: "pointer",
          fontSize: "16px",
        }}
      >
        Upload Audio
      </button>

      {file && (
        <div style={{ marginTop: "20px" }}>
          <h3>Selected File</h3>

          <p>
            <b>Name:</b> {file.name}
          </p>

          <p>
            <b>Size:</b> {(file.size / 1024).toFixed(2)} KB
          </p>
        </div>
      )}
    </div>
  );
}

export default AudioUpload;