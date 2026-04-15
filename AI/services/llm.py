from groq import Groq
import os
from dotenv import load_dotenv
load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)
def ask_llm(context, question, student):
    try:
        prompt = f"""
You are an AI Academic Advisor.

Student:
Semester: {student['semester']}
Department: {student['department']}

Context:
{context}

Question:
{question}
"""

        res = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are a helpful academic advisor."},
                {"role": "user", "content": prompt}
            ]
        )

        return res.choices[0].message.content

    except Exception as e:
        return f"Groq Error: {str(e)}"