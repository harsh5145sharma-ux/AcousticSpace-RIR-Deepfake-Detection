function Navbar() {
  return (
    <nav
      style={{
        background: "linear-gradient(90deg, #020617, #0F172A)",
        color: "white",
        padding: "18px 35px",
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center",
        boxShadow: "0 4px 15px rgba(0,0,0,0.25)"
      }}
    >
      <h2 style={{ margin: 0 }}>🎙 AcousticSpace</h2>

      <span
        style={{
          background: "#2563EB",
          padding: "8px 14px",
          borderRadius: "20px",
          fontSize: "14px"
        }}
      >
        AI Deepfake Detector
      </span>
    </nav>
  );
}

export default Navbar;