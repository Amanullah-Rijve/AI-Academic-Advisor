from groq import Groq
import os
import numpy as np
import faiss
import re
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
from services.pdf_loader import load_text

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# ---------------------------
# LOAD DATA
# ---------------------------
full_context = load_text("data/handbook.txt")

# Clean chunking
chunks = re.split(r"===+", full_context)
chunks = [c.strip() for c in chunks if len(c.strip()) > 30]

# ---------------------------
# EMBEDDING MODEL
# ---------------------------
embedder = SentenceTransformer("all-MiniLM-L6-v2")
embeddings = embedder.encode(chunks, convert_to_numpy=True)

dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(embeddings.astype("float32"))

# ---------------------------
# RETRIEVAL
# ---------------------------
def get_relevant_context(question: str, k: int = 5) -> str:
    q_vec = embedder.encode([question], convert_to_numpy=True)
    distances, indices = index.search(q_vec.astype("float32"), k)
    results = [chunks[i] for i in indices[0] if len(chunks[i].strip()) > 20]
    return "\n\n---\n\n".join(results)

# ---------------------------
# MAIN LLM FUNCTION
# ---------------------------
def ask_llm(question: str, student: dict) -> str:
    context = get_relevant_context(question)

    system_prompt = """You are an official Academic Advisor AI for Daffodil International University (DIU), Department of Software Engineering.

Your behavior rules:
- Answer ONLY using the provided CONTEXT
- If the answer is not in the context, respond exactly: "This information is not available in my dataset. Please contact the department directly."
- Never guess, assume, or fabricate information
- Be concise, structured, and professional
- Use bullet points when listing multiple items
- Always respond in the same language the student uses"""

    user_prompt = f"""Student Profile:
- Department: {student['department']}
- Semester: {student['semester']}

CONTEXT:
{context}

STUDENT QUESTION:
{question}

Provide a clear, accurate answer based strictly on the context above."""

    res = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.1,  # lower = more focused, less creative
        max_tokens=512
    )

    return res.choices[0].message.content.strip()