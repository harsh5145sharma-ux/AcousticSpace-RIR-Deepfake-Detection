import { useState } from "react";
import Navbar from "../components/Navbar";
import AudioUpload from "../components/AudioUpload";
import ResultCard from "../components/ResultCard";


function Dashboard() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [status, setStatus] = useState("Not Tested");
  const [confidence, setConfidence] = useState(0);

  const handleDetection = () => {
    setStatus("Processing...");

    setTimeout(() => {
      setStatus("Real");
      setConfidence(95);
    }, 2000);
  };

  return (
    <>
      <Navbar />

      <div
        style={{
          backgroundColor: "#F8FAFC",
          minHeight: "100vh",
          width: "100%",
          boxSizing: "border-box",
          padding: "20px",
        }}
      >
        <div
          style={{
            backgroundColor: "#ffffff",
            borderRadius: "18px",
            padding: "35px",
            maxWidth: "1200px",
            margin: "0 auto",
            boxShadow: "0 6px 18px rgba(0,0,0,0.12)",
          }}
        >
          <h1
            style={{
              marginBottom: "10px",
              color: "#1F2937",
            }}
          >
            AcousticSpace Dashboard
          </h1>

          <p
            style={{
              color: "#6B7280",
              marginBottom: "35px",
            }}
          >
            Welcome to the Audio Deepfake Detection System
          </p>

          <div
            style={{
              display: "flex",
              justifyContent: "space-between",
              alignItems: "flex-start",
              gap: "30px",
              flexWrap: "wrap",
            }}
          >
            {/* Left Side */}

            <div
              style={{
                flex: 1,
                minWidth: "350px",
              }}
            >
              <AudioUpload 
                   onUpload={handleDetection}
                   selectedFile={selectedFile}
                   setSelectedFile={setSelectedFile}
                 />

              <div style={{ marginTop: "25px" }}>
                <h2
                  style={{
                    color: "#2563EB",
                  }}
                >
                  Audio Information
                </h2>

                <p>
                    <strong>File Name:</strong>{" "}
                      {selectedFile ? selectedFile.name : "Not Selected"}
                </p>

                <p>
                  <b>Duration:</b> --:--
                </p>

                <p>
                   <strong>File Size:</strong>{" "}
                     {selectedFile
                     ? (selectedFile.size / 1024).toFixed(2) + " KB"
                      : "0 KB"}
                </p>
              </div>
            </div>

            {/* Right Side */}

            <div
              style={{
                flex: 1,
                minWidth: "320px",
              }}
            >
              <ResultCard
                status={status}
                confidence={confidence}
              />
            </div>
          </div>

          <div
            style={{
              marginTop: "50px",
              textAlign: "center",
              color: "#9CA3AF",
            }}
          >
            AcousticSpace © 2026
          </div>
        </div>
      </div>
    </>
  );
}

export default Dashboard;