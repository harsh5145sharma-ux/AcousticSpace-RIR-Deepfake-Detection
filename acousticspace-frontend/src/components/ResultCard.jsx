function ResultCard({ status, confidence }) {
  const color =
    status === "Real"
      ? "#22C55E"
      : status === "Fake"
      ? "#EF4444"
      : "#F59E0B";

  return (
    <div
      style={{
        background: "#fff",
        padding: "25px",
        borderRadius: "15px",
        boxShadow: "0 2px 10px rgba(0,0,0,0.1)",
      }}
    >
      <h2 style={{ color: "#2563EB" }}>
        🎯 Detection Result
      </h2>

      <p style={{ fontSize: "20px" }}>
        <strong>Status:</strong>{" "}
        <span style={{ color }}>{status}</span>
      </p>

      <p style={{ fontSize: "18px" }}>
        <strong>Confidence:</strong> {confidence}%
      </p>

      <progress
        value={confidence}
        max="100"
        style={{
          width: "100%",
          height: "18px",
          marginTop: "15px",
        }}
      />
    </div>
  );
}

export default ResultCard;