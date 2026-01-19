from dotenv import load_dotenv
from typing import Union,Optional
from pydantic import BaseModel
from fastapi import FastAPI
from app.services.chunking import chunker
from app.services.embedding import embed
from app.utils.search import sim_search
from app.utils.load import load_chunks
from app.prompt_builder import build_prompt
from app.services.generation import call_gemini
import os
import psycopg2

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

conn=psycopg2.connect(os.getenv("DATABASE_URL"))

class AnalyzeReq(BaseModel):
    readme:str
    docs:str
    code_of_conduct:Optional[str]= None
    
@app.post("/analyze")
def analyze(req:AnalyzeReq):
    readme_chunks=chunker(req.readme)
    docs_chunks=chunker(req.docs)
    if(req.code_of_conduct):
        coc_chunks=chunker(req.code_of_conduct)

    return {
        "readme_chunks": readme_chunks,
        "docs_chunks": docs_chunks,
        "coc_chunks": coc_chunks
    }

class ValidateReq(BaseModel):
    repo_id:str
    diff:str
@app.post("/validate")
def validate(req:ValidateReq):
    #get the diff/code change
    diff=req.diff

    #load the saved chunks of readme/coc/guidelines from db
    chunks=load_chunks(conn,req.repo_id)

    #get the top k chunks to reason on
    relevant_chunk=sim_search(diff,chunks)

    #build the prompt
    prompt=build_prompt(relevant_chunk,diff=diff)

    #call the ai api key
    generation=call_gemini(prompt=prompt)


    


    


