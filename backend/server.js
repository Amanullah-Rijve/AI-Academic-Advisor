import express from "express";
import cors from "cors";
import axios from "axios";
import db from "./db.js";

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

    const answer = aiRes.data.answer;

    db.query(
    "INSERT INTO chats (student_id, question, answer) VALUES (?,?,?)",
    [student_id, question, answer]
    );

    res.json({ answer });

} catch (err) {
    console.error(err);
    res.status(500).send("Error");
}
});

app.listen(5000, () => console.log("Server running on port 5000"));