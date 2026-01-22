from app.services.validator import run_validate
from app.models.validation import Validation
from app.db import get_conn

def validate_local(diff:str):
    connect=get_conn()
    return run_validate(
        repo_id="local",
        diff=diff,
        connect=connect
    )

