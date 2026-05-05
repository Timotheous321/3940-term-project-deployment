import { useState } from "react";
import "./App.css";
const API_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:5000";

function App() {
  const [username, setUsername] = useState("admin");
  const [password, setPassword] = useState("password123");
  const [token, setToken] = useState("");
  const [message, setMessage] = useState("");
  const [data, setData] = useState([]);
  const [error, setError] = useState("");

  async function handleLogin(e) {
    e.preventDefault();
    setError("");

    try {
      const response = await fetch(`${API_URL}/login`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          username: username,
          password: password,
        }),
      });

      const result = await response.json();

      if (!response.ok) {
        setError(result.error || "Login failed");
        return;
      }

      setToken(result.token);
      setMessage("Login successful. User authenticated.");
    } catch (err) {
      setError("Could not connect to backend.");
    }
  }

  async function getProtectedMessage() {
    setError("");

    try {
      const response = await fetch(`${API_URL}/api/message`, {
        method: "GET",
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      const result = await response.json();

      if (!response.ok) {
        setError(result.error || "Request failed");
        return;
      }

      setMessage(result.message);
      setData(result.data);
    } catch (err) {
      setError("Could not connect to backend.");
    }
  }

  function logout() {
    setToken("");
    setMessage("");
    setData([]);
    setError("");
  }

  return (
    <main className="page">
      <section className="card">
        <h1>The Realm of Suffering</h1>
        <p className="subtitle">
          A dark and mysterious place where I continue to suffer. 
        </p>

        {!token ? (
          <form onSubmit={handleLogin} className="form">
            <label>
              Username
              <input
                value={username}
                onChange={(e) => setUsername(e.target.value)}
              />
            </label>

            <label>
              Password
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
            </label>

            <button type="submit">Log In</button>
          </form>
        ) : (
          <div className="dashboard">
            <p className="success">You are logged in.</p>

            <button onClick={getProtectedMessage}>
              GET Request
            </button>

            <button className="secondary" onClick={logout}>
              Log Out
            </button>
          </div>
        )}

        {message && <p className="message">{message}</p>}

        {data.length > 0 && (
          <div className="data-box">
            <h2>Data from database:</h2>
            {data.map((item, index) => (
              <p key={index}>{item}</p>
            ))}
          </div>
        )}

        {error && <p className="error">{error}</p>}
      </section>
    </main>
  );
}

export default App;