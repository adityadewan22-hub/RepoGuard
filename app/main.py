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
from app.models.validation import Validation
from app.db import init_db
from app.utils.store import store_chunks
from app.services.embedding import embed
from app.models.chunk import Chunk
from app.db import connect
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
    repo_id:str
    readme:str
    docs:str
    code_of_conduct:Optional[str]= None
    
@app.post("/analyze")
def analyze(req:AnalyzeReq):
    all_chunks:list[Chunk]=[]

    readme_chunks=chunker(req.readme,authority="README")
    contributing_chunks=chunker(req.docs,authority="CONTRIBUTING")
    coc_chunks:list[Chunk]=[]

    if(req.code_of_conduct):
        coc_chunks=chunker(req.code_of_conduct,authority="CODE OF CONDUCT")
    
    all_chunks.extend(readme_chunks)
    all_chunks.extend(contributing_chunks)
    if(len(coc_chunks)):
        all_chunks.extend(coc_chunks)

    #initialise db
    init_db()

    #embed chunk
    embeddings = embed([c.content for c in all_chunks])
    for chunk, emb in zip(all_chunks, embeddings):
      chunk.embedding = emb

    #store chunks
    store_chunks(connect,req.repo_id,all_chunks)

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
    print("RAW MODEL OUTPUT:\n", generation)

    try:
      raw = generation.strip()

      # Remove markdown code fences
      if raw.startswith("```"):
        raw = raw.split("```")[1].strip()

      # Trim to JSON object
      start = raw.find("{")
      end = raw.rfind("}") + 1
      raw = raw[start:end]
      result = Validation.model_validate_json(raw)
      return result
    except Exception as e:
      print("PARSING ERROR:", e)
      return Validation(
        status="Warning",
        explanation="Validator could not produce a structured response.",
        violated_guidelines=[]
      )
    


    


    


