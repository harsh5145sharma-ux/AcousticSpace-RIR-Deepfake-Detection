import "../styles/WaveformViewer.css";
import { useEffect, useRef, useState } from "react";
import WaveSurfer from "wavesurfer.js";

function WaveformViewer({ selectedFile, result }) {
  const waveformRef = useRef(null);
  const waveSurferRef = useRef(null);
  const [audioUrl, setAudioUrl] = useState(null);

  useEffect(() => {
    if (!selectedFile) {
      setAudioUrl(null);
      return;
    }

    if (waveSurferRef.current) {
      waveSurferRef.current.destroy();
    }

    const url = URL.createObjectURL(selectedFile);
    setAudioUrl(url);

    const wavesurfer = WaveSurfer.create({
      container: waveformRef.current,
      waveColor: "#93C5FD",
      progressColor: "#2563EB",
      cursorColor: "#1E40AF",
      height: 100,
    });

    waveSurferRef.current = wavesurfer;
    wavesurfer.load(url);

    return () => {
      wavesurfer.destroy();
      URL.revokeObjectURL(url);
    };
  }, [selectedFile]);

  return (
    <div className="waveform-card">

      <h2 className="waveform-title">
        🎵 Audio Waveform
      </h2>

      {selectedFile ? (
        <>
          <div ref={waveformRef}></div>

          {audioUrl && (
           <audio
              controls
              src={audioUrl}
              className="audio-player"
            />
)}

          
        </>
      ) : (
        <p className="no-audio">
          Please upload an audio file.
        </p>
      )}

    </div>
  );
}

export default WaveformViewer;