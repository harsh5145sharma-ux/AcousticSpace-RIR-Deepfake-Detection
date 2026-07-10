function ResultCard() {
  return (
    <div
      style={{
        marginTop: "20px",
        padding: "20px",
        border: "1px solid #ccc",
        borderRadius: "8px",
        width: "300px"
      }}
    >
      <h3>Detection Result</h3>
      <p>Status: Not Tested</p>
      <p>Confidence: 0%</p>
    </div>
  );
}

export default ResultCard;