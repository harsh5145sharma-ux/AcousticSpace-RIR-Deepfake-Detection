import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import API from "../api/api";
import "../styles/Signup.css";

function Signup() {
  const navigate = useNavigate();

  const [showPassword, setShowPassword] = useState(false);

  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSignup = async (e) => {
  e.preventDefault();

  setError("");

  try {
    setLoading(true);

    await API.post("/auth/signup", {
      username,
      email,
      password,
    });

    alert("Account Created Successfully");

    navigate("/login");

  } catch (err) {
    setError(err.response?.data?.detail || "Signup Failed");
  } finally {
    setLoading(false);
  }
};


  return (
    <div className="signup-container">
      <div className="signup-card">

        <h1 className="signup-logo">🎧 AcousticSpace</h1>

        <h2 className="signup-title">
          Create Account
        </h2>

        <p className="signup-subtitle">
          Register to access the Audio Deepfake Detection System
        </p>

        <form onSubmit={handleSignup}>

          <div className="input-group">
            <label>Username</label>
            <input
              type="text"
              placeholder="Enter username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
            />
          </div>

          <div className="input-group">
            <label>Email</label>
            <input
              type="email"
              placeholder="Enter email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
          </div>

          <div className="input-group">

            <label>Password</label>

            <div className="password-box">

              <input
                type={showPassword ? "text" : "password"}
                placeholder="Create password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />

              <button
                type="button"
                className="show-btn"
                onClick={() =>
                  setShowPassword(!showPassword)
                }
              >
                {showPassword ? "Hide" : "Show"}
              </button>

            </div>

          </div>
          {error && (
            <p className="error-message">
              {error}
            </p>
          )}

          <button
            type="submit"
            className="signup-btn"
            disabled={loading}
          >
            {loading ? "Creating..." : "Create Account"}
          </button>

        </form>

        <p className="login-text">

          Already have an account?

          <Link to="/login">
            {" "}Login
          </Link>

        </p>

      </div>
    </div>
  );
}

export default Signup;