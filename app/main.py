from dotenv import load_dotenv
from typing import Union,Optional
from pydantic import BaseModel
from fastapi import FastAPI
from app.services.chunking import chunker
import os

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

class AnalyzeRequest(BaseModel):
    readme:str
    docs:str
    code_of_conduct:Optional[str]= None
    

@app.post("/analyze")
def analyze(req:AnalyzeRequest):
    readme_chunks=chunker(req.readme)
    docs_chunks=chunker(req.docs)
    if(req.code_of_conduct):
        coc_chunks=chunker(req.code_of_conduct)

    return {
        "readme_chunks": readme_chunks,
        "docs_chunks": docs_chunks,
        "coc_chunks": coc_chunks
    }
