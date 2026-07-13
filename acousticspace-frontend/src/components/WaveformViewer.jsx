import { useEffect, useRef } from "react";
import WaveSurfer from "wavesurfer.js";

function WaveformViewer({ selectedFile, result }) {
  const waveformRef = useRef(null);
  const waveSurferRef = useRef(null);

  useEffect(() => {
    if (!selectedFile) return;

    if (waveSurferRef.current) {
      waveSurferRef.current.destroy();
    }

    const wavesurfer = WaveSurfer.create({
      container: waveformRef.current,
      waveColor: "#93C5FD",
      progressColor: "#2563EB",
      cursorColor: "#1E40AF",
      height: 100,
    });

    waveSurferRef.current = wavesurfer;

    const audioUrl = URL.createObjectURL(selectedFile);
    wavesurfer.load(audioUrl);

    return () => {
      wavesurfer.destroy();
      URL.revokeObjectURL(audioUrl);
    };
  }, [selectedFile]);

  return (
    <div
      style={{
        background: "#fff",
        padding: "20px",
        borderRadius: "12px",
        marginTop: "20px",
      }}
    >
      <h2 style={{ color: "#2563EB" }}>Waveform</h2>

      {selectedFile ? (
  <>
    <div ref={waveformRef}></div>

    <audio
      controls
      src={URL.createObjectURL(selectedFile)}
      style={{
        width: "100%",
        marginTop: "20px",
      }}
    />
    {result && (
  <div
    style={{
      marginTop: "20px",
      backgroundColor: "#F8FAFC",
      padding: "15px",
      borderRadius: "10px",
    }}
  >
    <h3 style={{ color: "#2563EB" }}>
      Suspicious Segments
    </h3>

    {result.flagged_segments.map((segment, index) => (
      <p key={index}>
        🔴 {segment[0]} sec - {segment[1]} sec
      </p>
    ))}
  </div>
)}
  </>
) : (
  <p>Please upload an audio file.</p>
)}
    </div>
  );
}

export default WaveformViewer;