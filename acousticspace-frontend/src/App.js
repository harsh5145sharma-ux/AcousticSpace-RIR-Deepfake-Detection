import "./App.css";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";

import Login from "./pages/Login";
import Signup from "./pages/Signup";
import Dashboard from "./pages/Dashboard";
import History from "./pages/History";

function App() {
  return (
    <BrowserRouter>
      <Routes>

        {/* Default Route */}
        <Route path="/" element={<Navigate to="/login" />} />

        {/* Authentication */}
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />

        {/* Dashboard */}
        <Route
          path="/dashboard"
          element={
          localStorage.getItem("token")
            ? <Dashboard />
            : <Navigate to="/login" />
          }
        />
        <Route
           path="/history"
           element={
           localStorage.getItem("token")
             ? <History />
             : <Navigate to="/login" />
           }
        />

      </Routes>
    </BrowserRouter>
  );
}

export default App;