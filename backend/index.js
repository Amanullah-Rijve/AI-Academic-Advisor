import express from "express";
import cors from "cors";
import axios from "axios";
import {db} from "./db.js";

const app = express();
app.use(cors());
app.use(express.json());

app.post("/ask", async (req, res) => {
  const { student_id, question, semester, department } = req.body;

  try {
    const aiRes = await axios.post("http://localhost:8000/ask", {
      question,
      semester,
      department
    });

    console.log("FASTAPI RESPONSE:", aiRes.data);

    return res.json({
      answer: aiRes.data.answer
    });

  } catch (err) {
    console.error("EXPRESS ERROR:", err.message);
    res.status(500).json({ error: "Server error" });
  }
});

app.listen(5000, () => console.log("Server running on port 5000"));