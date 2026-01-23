# repoguard/run.py
import requests
from app.models.validation import Validation

REPOGUARD_API = "https://repoguard.dev/validate"  # your FastAPI server

def validate_remote(diff: str) -> Validation:
    resp = requests.post(
        REPOGUARD_API,
        json={"diff": diff},
        timeout=30,
    )
    resp.raise_for_status()
    return Validation.model_validate(resp.json())
