import "../styles/ResultCard.css";

function ResultCard({
  status,
  confidence,
  selectedFile,
  detectionTime,
}) {
  const color =
    status === "Real"
      ? "#22C55E"
      : status === "Fake"
      ? "#EF4444"
      : "#F59E0B";

  const downloadReport = () => {
    const report = `
AcousticSpace Detection Report

---------------------------------

File Name : ${selectedFile ? selectedFile.name : "No File"}

Status : ${status}

Confidence : ${confidence.toFixed(0)}%

Generated :
${detectionTime}

---------------------------------

This report is generated for demo purposes.
`;

    const blob = new Blob([report], {
      type: "text/plain",
    });

    const url = URL.createObjectURL(blob);

    const a = document.createElement("a");
    a.href = url;
    a.download = "Detection_Report.txt";
    a.click();

    URL.revokeObjectURL(url);
  };

  return (
    <div className="result-card">

      <h2 className="result-title">
        🎯 Detection Result
      </h2>
      <p className="result-description">
       AI model prediction based on uploaded audio.
      </p>

      <div
        className="status-badge"
        style={{ backgroundColor: color }}
      >
        {status}
      </div>

      <div
        className="confidence-circle"
        style={{
          borderColor: color,
          color: color,
        }}
      >
        {status === "Not Tested" ? "-" : `${confidence}%`}
      </div>

      <p className="confidence-title">
        Confidence Score
      </p>

      <progress
        className="confidence-progress"
        value={confidence}
        max="100"
      />

      <p className="detection-time">
        <strong>Detection Time:</strong>{" "}
        {detectionTime}
      </p>
      <p>
        <strong>Filename:</strong>{" "}
        {selectedFile ? selectedFile.name : "-"}
      </p>

      <p className="analysis-message">
        {status === "Not Tested"
          ? "Upload an audio file to start detection."
          : "AI analysis completed successfully."}
      </p>

      <button
        onClick={downloadReport}
        disabled={
          !selectedFile || status === "Not Tested"
        }
        className="download-btn"
      >
        📄 Download Report
      </button>

    </div>
  );
}

export default ResultCard;