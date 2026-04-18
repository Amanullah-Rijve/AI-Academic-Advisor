from fastapi import FastAPI
from pydantic import BaseModel
from services.llm import ask_llm

app = FastAPI()

class Query(BaseModel):
    question: str
    semester: int
    department: str

@app.post("/ask")
def ask(q: Query):
    try:
        student = {
            "semester": q.semester,
            "department": q.department
        }

        answer = ask_llm(q.question, student)

        return {"answer": answer}

    except Exception as e:
        return {"answer": f"Server error: {str(e)}"}