import { useState } from "react";
import Navbar from "../components/Navbar";
import AudioUpload from "../components/AudioUpload";
import ResultCard from "../components/ResultCard";
import WaveformViewer from "../components/WaveformViewer";
import mockResult from "../data/mockResult";
import "../styles/Dashboard.css";

function Dashboard() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [status, setStatus] = useState("Not Tested");
  const [confidence, setConfidence] = useState(0);
  const [detectionTime, setDetectionTime] = useState("-");
  const [duration, setDuration] = useState("--:--");
  const [isProcessing, setIsProcessing] = useState(false);
  const [result, setResult] = useState(null);
  const [message, setMessage] = useState("");
  

  const handleDetection = () => {
    setStatus("Processing...");
    setConfidence(0);
    setResult(null);
    setIsProcessing(true);
    setMessage("Audio uploaded successfully!");

    setTimeout(() => {
      setResult(mockResult);
      setStatus(mockResult.is_fake ? "Fake" : "Real");
      setConfidence(mockResult.confidence);
      setDetectionTime(new Date().toLocaleString());
      setIsProcessing(false);
      setMessage("Detection Completed Successfully!");
    }, 2000);
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
                  : `${confidence}%`}
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
                    Processing Audio...
                  </h3>

                  <h3 className="processing-title">
                    ⏳ Processing Audio...
                 </h3>

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
            © 2026 AcousticSpace Team
          </p>

          </div>

        </div>

      </div>
    </>
  );
}

export default Dashboard;