import Navbar from "../components/Navbar";
import {useState} from "react";
import AudioUpload from "../components/AudioUpload";
import ResultCard from "../components/ResultCard";

function Dashboard() {
  const [selectedFile,setSelectedFile]=useState(null);
  return (
    <>
      <Navbar />

      <div
        style={{
          backgroundColor: "#F5F7FA",
          minHeight: "100vh",
          padding: "40px",
        }}
      >
        <div
          style={{
            backgroundColor: "#ffffff",
            borderRadius: "18px",
            padding: "35px",
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
              gap: "40px",
              flexWrap: "wrap",
              alignItems: "flex-start",
            }}
          >
            {/* Left Side */}
            <div
              style={{
                flex: "1",
                minWidth: "350px",
              }}
            >
              <AudioUpload />

              <div
                style={{
                  marginTop: "30px",
                  backgroundColor: "#F9FAFB",
                  padding: "20px",
                  borderRadius: "12px",
                  boxShadow: "0 2px 8px rgba(0,0,0,0.08)",
                }}
              >
                <h2 style={{ color: "#2563EB" }}>
                  Audio Information
                </h2>

                <p>
                  <b>File Name:</b> Not Selected
                </p>

                <p>
                  <b>Duration:</b> --:--
                </p>

                <p>
                  <b>File Size:</b> 0 KB
                </p>
              </div>
            </div>

            {/* Right Side */}
            <div
              style={{
                flex: "1",
                minWidth: "320px",
              }}
            >
              <ResultCard />
            </div>
          </div>
        </div>
      </div>
    </>
  );
}

export default Dashboard;