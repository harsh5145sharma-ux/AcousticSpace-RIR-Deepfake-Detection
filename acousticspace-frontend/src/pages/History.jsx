import { useEffect, useState } from "react";
import API from "../api/api";
import Navbar from "../components/Navbar";
import "../styles/History.css";

function History() {
  const [history, setHistory] = useState([]);
  const [filteredHistory, setFilteredHistory] = useState([]);
  const [search, setSearch] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadHistory();
  }, []);

  useEffect(() => {
    setFilteredHistory(
      history.filter((item) =>
        item.filename.toLowerCase().includes(search.toLowerCase())
      )
    );
  }, [search, history]);

  const loadHistory = async () => {
    try {
      const token = localStorage.getItem("token");

      const res = await API.get("/history/", {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      setHistory(res.data);
      setFilteredHistory(res.data);
    } catch (err) {
      console.log(err);
      alert("Unable to load history");
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <Navbar />

      <div className="history-container">

        <div className="history-card">

          <h2 className="history-title">
            📜 Prediction History
          </h2>

          <input
            type="text"
            placeholder="🔍 Search by filename..."
            className="history-search"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />

          {loading ? (
            <p className="loading-text">Loading...</p>
          ) : filteredHistory.length === 0 ? (
            <div className="empty-box">
              <h3>📂 No Prediction History Found</h3>
              <p>Upload an audio file first.</p>
            </div>
          ) : (
            <table className="history-table">

              <thead>

                <tr>
                  <th>File Name</th>
                  <th>Prediction</th>
                  <th>Confidence</th>
                  <th>Date</th>
                </tr>

              </thead>

              <tbody>

                {filteredHistory.map((item) => (

                  <tr key={item.id}>

                    <td>{item.filename}</td>

                    <td>

                      <span
                        className={
                          item.result.toLowerCase() === "fake"
                            ? "badge fake"
                            : "badge real"
                        }
                      >
                        {item.result.toUpperCase()}
                      </span>

                    </td>

                    <td>
                      {(item.confidence * 100).toFixed(0)}%
                    </td>

                    <td>
                      {new Date(item.created_at).toLocaleString()}
                    </td>

                  </tr>

                ))}

              </tbody>

            </table>
          )}

        </div>

      </div>
    </>
  );
}

export default History;