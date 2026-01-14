from dotenv import load_dotenv
from typing import Union
from pydantic import BaseModel
from fastapi import FastAPI
from app.services.chunking import chunker
import os


load_dotenv()

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

print(os.getenv("GEMINI_API_KEY"))

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

class AnalyzeRequest(BaseModel):
    resume_text:str
    jd_text:str

@app.post("/analyze")
def analyze(req:AnalyzeRequest):
    resume_chunks=chunker(req.resume_text)
    jd_chunks=chunker(req.jd_text)

    return {
        "resume_chunks": resume_chunks,
        "jd_chunks": jd_chunks
    }
