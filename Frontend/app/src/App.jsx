import React, { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState([]);
  const [department, setDepartment] = useState("CSE");
  const [semester, setSemester] = useState("");
  const [batch, setBatch] = useState("");
  const [loading, setLoading] = useState(false);

  const send = async () => {
    if (!question.trim()) return;

    const userMsg = { type: "user", text: question };
    setMessages((prev) => [...prev, userMsg]);
    setLoading(true);

    try {
     const res = await axios.post("http://localhost:5000/ask", {
  student_id: 1,
  question,
  semester,
  department,
});

      const botMsg = { type: "bot", text: res.data.answer };
      setMessages((prev) => [...prev, botMsg]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        { type: "bot", text: "Server error" },
      ]);
    }

    setLoading(false);
    setQuestion("");
  };

  return (
    <div className="container">
      {/* SIDEBAR */}
      <div className="sidebar">
        <h2>🎓 Profile</h2>

        <select
          value={department}
          onChange={(e) => setDepartment(e.target.value)}
        >
          <option>CSE</option>
          <option>CIS</option>
          <option>SWE</option>
          <option>MCT</option>
          <option>ITM</option>
        </select>

        <input
          placeholder="Semester"
          value={semester}
          onChange={(e) => setSemester(e.target.value)}
        />

        <input
          placeholder="Batch"
          value={batch}
          onChange={(e) => setBatch(e.target.value)}
        />
      </div>

      {/* CHAT */}
      <div className="chat">
        <div className="header">🎓 Smart Academic Advisor</div>

        <div className="messages">
          {messages.map((m, i) => (
            <div key={i} className={`msg ${m.type}`}>
              {m.text}
            </div>
          ))}

          {loading && <div className="loading">AI is thinking...</div>}
        </div>

        <div className="input-area">
          <input
            value={question}
            placeholder="Ask about courses, GPA, credits..."
            onChange={(e) => setQuestion(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && send()}
          />
          <button onClick={send}>Send</button>
        </div>
      </div>
    </div>
  );
}

export default App;