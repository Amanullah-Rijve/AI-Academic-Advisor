from fastapi import FastAPI
from pydantic import BaseModel
from services.llm import ask_llm
from services.pdf_loader import load_pdf


app = FastAPI()

context = load_pdf("data/handbook.pdf")

class Query(BaseModel):
    question: str
    semester: int
    department: str


@app.post("/ask")
def ask(q: Query):
    try:
        print("REQUEST:", q)

        student = {
            "semester": q.semester,
            "department": q.department
        }

        answer = ask_llm(context, q.question, student)

        print("ANSWER:", answer)

        return {"answer": answer}

    except Exception as e:
        print("FASTAPI ERROR:", str(e))
        return {"error": str(e)}