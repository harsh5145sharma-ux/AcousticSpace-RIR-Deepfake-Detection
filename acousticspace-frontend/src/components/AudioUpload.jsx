import { useRef } from "react";
import "../styles/AudioUpload.css";

function AudioUpload({
  selectedFile,
  setSelectedFile,
  onUpload,
  setDuration,
  isProcessing,
}) {
  const fileInputRef = useRef(null);

  const handleFileChange = (event) => {
    const file = event.target.files[0];

    if (file) {
      setSelectedFile(file);

      const audio = new Audio(URL.createObjectURL(file));

      audio.onloadedmetadata = () => {
        const minutes = Math.floor(audio.duration / 60);
        const seconds = Math.floor(audio.duration % 60);

        if (setDuration) {
          setDuration(
            `${minutes}:${seconds.toString().padStart(2, "0")}`
          );
        }

        URL.revokeObjectURL(audio.src);
      };
    }
  };

  const handleUpload = () => {
    if (!selectedFile) {
      alert("Please select an audio file first!");
      return;
    }

  

    if (onUpload) {
      onUpload();
    }
  };

  return (
    <div className="upload-card">
      <h2 className="upload-title">🎵 Upload Audio</h2>

      <p className="upload-subtitle">
        Upload an audio recording to detect whether it is
        Real or AI Generated.
      </p>

      <label
        htmlFor="audioFile"
        className="choose-file-btn"
      >
        📁 Choose Audio File
      </label>

      <input
        ref={fileInputRef}
        id="audioFile"
        type="file"
        accept=".wav,.mp3"
        onChange={handleFileChange}
        className="hidden-input"
      />

      <br />
      <br />

      <button
        onClick={handleUpload}
        disabled={!selectedFile || isProcessing}
        className="upload-btn"
      >
        {isProcessing ? "⏳ Uploading..." : "🚀 Upload Audio"}
      </button>

      {selectedFile && (
        <div className="selected-file-card">
          <h3>Selected File</h3>

          <p>
            <b>Name:</b> {selectedFile.name}
          </p>

          <p>
            <b>Size:</b>{" "}
            {(selectedFile.size / 1024).toFixed(2)} KB
          </p>

          <p>
            <b>Type:</b> {selectedFile.type}
          </p>

          <hr />

          <p>
            <b>Supported:</b> WAV, MP3
          </p>

          <p>
            <b>Maximum Size:</b> 20 MB
          </p>

          <p>
            <b>AI Model:</b> CNN + BiLSTM
          </p>

          <p>
            <b>Status:</b>{" "}
            {isProcessing ? "Analyzing Audio..." : "Ready for Analysis"}
          </p>
          
        </div>
      )}
    </div>
  );
}

export default AudioUpload;