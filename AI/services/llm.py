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

# Better chunking (clean + stable)
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
# RETRIEVAL (FIXED)
# ---------------------------
def get_relevant_context(question, k=5):
    q_vec = embedder.encode([question], convert_to_numpy=True)

    distances, indices = index.search(q_vec.astype("float32"), k)

    results = [chunks[i] for i in indices[0]]

    # REMOVE junk empty chunks
    results = [r for r in results if len(r.strip()) > 20]

    return "\n\n".join(results)

# ---------------------------
# MAIN LLM FUNCTION (FIXED)
# ---------------------------
def ask_llm(question, student):
    context = get_relevant_context(question)

    prompt = f"""
You are a DIU Academic Advisor AI.

You MUST follow these rules:
- Answer ONLY using the CONTEXT below
- If answer is not found, say: "I don't know from dataset"
- Do NOT guess
- Be short, clear, helpful

Student Info:
- Semester: {student['semester']}
- Department: {student['department']}

CONTEXT:
{context}

QUESTION:
{question}

FINAL ANSWER:
"""

    res = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You are a strict academic advisor AI."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    return res.choices[0].message.content.strip()