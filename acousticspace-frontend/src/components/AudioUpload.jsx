import { useRef } from "react";

function AudioUpload({ selectedFile, setSelectedFile, onUpload }) {

  const fileInputRef = useRef(null);

  const handleFileChange = (event) => {
    const file = event.target.files[0];

    if (file) {
      setSelectedFile(file);
    }
  };

  const handleUpload = () => {
    if (!selectedFile) {
      alert("Please select an audio file first!");
      return;
    }

    alert(`${selectedFile.name} uploaded successfully!`);

    if (onUpload) {
      onUpload();
    }

    
  };

  return (
    <div
      style={{
        backgroundColor: "#ffffff",
        padding: "20px",
        borderRadius: "15px",
        boxShadow: "0 2px 10px rgba(0,0,0,0.1)",
      }}
    >
      <h2 style={{ color: "#2563EB" }}>Upload Audio</h2>

      <p>Select a WAV or MP3 file for AI analysis.</p>

      <label
        htmlFor="audioFile"
        style={{
          backgroundColor: "#2563EB",
          color: "white",
          padding: "12px 20px",
          borderRadius: "8px",
          cursor: "pointer",
          display: "inline-block",
          marginBottom: "15px",
        }}
      >
        📁 Choose Audio File
      </label>

      <input
        ref={fileInputRef}
        id="audioFile"
        type="file"
        accept=".wav,.mp3"
        onChange={handleFileChange}
        style={{ display: "none" }}
      />

      <br />
      <br />

      <button
        onClick={handleUpload}
        disabled={!selectedFile}
        style={{
          backgroundColor: "#2563EB",
          color: "white",
          border: "none",
          padding: "14px 28px",
          borderRadius: "10px",
          cursor: selectedFile ? "pointer" : "not-allowed",
          fontSize: "16px",
          opacity: selectedFile ? 1 : 0.6,
        }}
      >
        Upload Audio
      </button>

      {selectedFile && (
        <div style={{ marginTop: "25px" }}>
          <h3>Selected File</h3>

          <p><b>Name:</b> {selectedFile.name}</p>

          <p>
            <b>Size:</b> {(selectedFile.size / 1024).toFixed(2)} KB
          </p>

          <p>
            <b>Type:</b> {selectedFile.type}
          </p>
        </div>
      )}
    </div>
  );
}

export default AudioUpload;