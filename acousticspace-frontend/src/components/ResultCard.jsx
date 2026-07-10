function ResultCard({ status, confidence }) {
  return (
    <div
      style={{
        backgroundColor: "#ffffff",
        padding: "30px",
        minWidth: "280px",
        borderRadius: "15px",
        boxShadow: "0 4px 12px rgba(0,0,0,0.08)",
        minHeight: "250px",
      }}
    >
      <h2 style={{ color: "#2563EB" }}>
        🎯 Detection Result
      </h2>

      <p>
        <b>Status:</b> {status}
      </p>

      <p>
        <b>Confidence:</b> {confidence}%
      </p>
    </div>
  );
}

export default ResultCard;