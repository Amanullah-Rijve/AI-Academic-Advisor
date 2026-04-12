from fastapi import FastAPI
from pydantic import BaseModel
from services.llm import ask_llm
from services.pdf_loader import load_pdf


app = FastAPI()

context = load_pdf("data/handbook.pdf")

class Query(BaseModel):
    question: int
    semester : int
    dapartment: str
    
@app.post("/ask")
def ask(q:Query):
    Student={
        "semester":q.semester,
        "department":q.department
    }
    answer = ask_llm(context,q.question,Student)   
    return{"answer":answer}
        