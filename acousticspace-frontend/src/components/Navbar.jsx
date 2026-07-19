import "../styles/Navbar.css";

function Navbar() {
  return (
    <nav className="navbar">
      <div className="logo">
        🎧 AcousticSpace
      </div>

      <div className="version">
        Audio Deepfake Detection v1.0
      </div>
    </nav>
  );
}

export default Navbar;