import { useState } from "react";
import Navbar from "../components/Navbar";
import AudioUpload from "../components/AudioUpload";
import ResultCard from "../components/ResultCard";
import WaveformViewer from "../components/WaveformViewer";
import API from "../api/api";
import "../styles/Dashboard.css";
import { useNavigate } from "react-router-dom";

function Dashboard() {
  const navigate = useNavigate();
  const [selectedFile, setSelectedFile] = useState(null);
  const [status, setStatus] = useState("Not Tested");
  const [confidence, setConfidence] = useState(0);
  const [detectionTime, setDetectionTime] = useState("-");
  const [duration, setDuration] = useState("--:--");
  const [isProcessing, setIsProcessing] = useState(false);
  const [result, setResult] = useState(null);
  const [message, setMessage] = useState("");
  

  const handleDetection = async () => {
  if (!selectedFile) {
    alert("Please select an audio file first!");
    return;
  }
  const token = localStorage.getItem("token");

  if (!token) {
    alert("Please login first!");
    return;
  }

  setStatus("Processing...");
  setConfidence(0);
  setResult(null);
  setIsProcessing(true);
  setMessage("");

  try {
    const formData = new FormData();
formData.append("file", selectedFile);

const response = await API.post("/predict/", formData, {
  headers: {
    Authorization: `Bearer ${token}`,
    "Content-Type": "multipart/form-data",
  },
});

const data = response.data;

    setResult(data);
    setStatus(
      data.prediction.toLowerCase() === "fake" ? "Fake" : "Real"
    );
    setConfidence(data.confidence * 100);
    setDetectionTime(new Date().toLocaleString());
    setMessage("Audio analyzed successfully. Prediction saved to history.");
    setTimeout(() => {
       setMessage("");
    }, 3000);
  } catch (error) {
    console.error(error);
    setStatus("Error");
    setMessage("Unable to connect to server. Please check backend and try again.");
  } finally {
    setIsProcessing(false);
  }
};

  return (
    <>
      <Navbar />

      <div className="dashboard-container">

        <div className="dashboard-card">

          <h1 className="dashboard-title">
            AcousticSpace Dashboard
          </h1>

          <p className="dashboard-subtitle">
            Welcome to the Audio Deepfake Detection System
          </p>

           {message && (
            <div className="success-message">
              ✅ {message}
            </div>
          )}

          {/* Summary Cards */}

          <div className="summary-cards">

            <div className="summary-card summary-blue">
              <h3 className="summary-title-blue">
                📁 Selected File
              </h3>

              <p>
                {selectedFile ? selectedFile.name : "No File Selected"}
              </p>
            </div>

            <div className="summary-card summary-green">
              <h3 className="summary-title-green">
                🎯 Status
              </h3>

              <p>{status}</p>
            </div>

            <div className="summary-card summary-yellow">
              <h3 className="summary-title-yellow">
                📊 Confidence
              </h3>

              <p>
                {status === "Not Tested"
                   ? "-"
                   : `${confidence.toFixed(0)}%`}
              </p>
            </div>

          </div>

          {/* Main Layout */}

          <div className="dashboard-content">

            {/* Left Panel */}

            <div className="left-panel">

              <AudioUpload
                selectedFile={selectedFile}
                setSelectedFile={setSelectedFile}
                setDuration={setDuration}
                onUpload={handleDetection}
                isProcessing={isProcessing}
              />

              <div className="audio-info">

                <h2 className="audio-info-title">
                  Audio Information
                </h2>

                <p>
                  <strong>File Name:</strong>{" "}
                  {selectedFile
                    ? selectedFile.name
                    : "Not Selected"}
                </p>

                <p>
                  <strong>Duration:</strong> {duration}
                </p>

                <p>
                  <strong>File Type:</strong>{" "}
                  {selectedFile
                    ? selectedFile.type
                    : "Not Available"}
                </p>

                <p>
                  <strong>File Size:</strong>{" "}
                  {selectedFile
                    ? `${(selectedFile.size / 1024).toFixed(2)} KB`
                    : "0 KB"}
                </p>

              </div>

              <WaveformViewer
                selectedFile={selectedFile}
                result={result}
              />

            </div>

            {/* Right Panel */}

            <div className="right-panel">

              {isProcessing && (

                <div className="processing-box">

                  <h3 className="processing-title">
                    ⏳ Analyzing Audio...
                  </h3>

                  <p>Please wait while AI analyzes your audio.</p>

                  <progress
                      className="processing-progress"
                  />

                </div>

              )}

              <ResultCard
                status={status}
                confidence={confidence}
                selectedFile={selectedFile}
                detectionTime={detectionTime}
              />

            </div>

          </div>
          <div style={{ textAlign: "center", marginTop: "20px" }}>
           <button
             onClick={() => navigate("/history")}
             style={{
               padding: "10px 20px",
               borderRadius: "8px",
               border: "none",
               cursor: "pointer",
               background: "#2563EB",
               color: "white",
               fontWeight: "bold",
            }}
          >
           📜 View Prediction History
          </button>
        </div>

          {/* Footer */}

          <div className="footer">

          <h3 className="footer-title">
           🎧 AcousticSpace
          </h3>

           <p>
           AI Powered Audio Deepfake Detection System
           </p>

           <p>
             Frontend Module • Member 4
           </p>

           <p>
             Version 1.0
           </p>

           <p>
            © 2026 AcousticSpace Team
          </p>

          </div>

        </div>

      </div>
    </>
  );
}

export default Dashboard;