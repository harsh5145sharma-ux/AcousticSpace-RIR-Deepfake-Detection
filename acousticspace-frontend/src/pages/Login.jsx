import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import API from "../api/api";
import "../styles/Login.css";

function Login() {
  const navigate = useNavigate();

  const [showPassword, setShowPassword] = useState(false);

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleLogin = async (e) => {
    e.preventDefault();

    setError("");

    if (!username || !password) {
      setError("Please fill all fields");
      return;
    }

    try {
      setLoading(true);

      const formData = new URLSearchParams();
      formData.append("username", username);
      formData.append("password", password);

      const res = await API.post("/auth/login", formData, {
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
      });

      localStorage.setItem("token", res.data.access_token);

      alert("Login Successful ✅");

      navigate("/dashboard");
    } catch (err) {
      console.log(err);

      setError(
        err.response?.data?.detail || "Login Failed"
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-container">

      <div className="login-card">

        <h1 className="login-logo">🎧 AcousticSpace</h1>

        <h2 className="login-title">
          Welcome Back
        </h2>

        <p className="login-subtitle">
          Login to continue Audio Deepfake Detection
        </p>

        {error && (
          <p className="error-message">
            {error}
          </p>
        )}

        <form onSubmit={handleLogin}>

          <div className="input-group">

            <label>Username</label>

            <input
              type="text"
              placeholder="Enter username"
              value={username}
              onChange={(e) =>
                setUsername(e.target.value)
              }
            />

          </div>

          <div className="input-group">

            <label>Password</label>

            <div className="password-box">

              <input
                type={showPassword ? "text" : "password"}
                placeholder="Enter password"
                value={password}
                onChange={(e) =>
                  setPassword(e.target.value)
                }
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

          <div className="login-options">

            <label>

              <input type="checkbox" />

              Remember Me

            </label>

            <a href="/">Forgot Password?</a>

          </div>

          <button
            type="submit"
            className="login-btn"
            disabled={loading}
          >
            {loading ? "Logging in..." : "Login"}
          </button>

        </form>

        <p className="signup-text">

          Don't have an account?

          <Link to="/signup">
            {" "}Sign Up
          </Link>

        </p>

      </div>

    </div>
  );
}

export default Login;