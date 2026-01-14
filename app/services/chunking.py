from fastapi import FastAPI

def chunker(text:str):
    chunks=[]
    sentences=text.split(".")
    for s in sentences:
        if(s):
            chunks.append(s)
    return chunks
    
