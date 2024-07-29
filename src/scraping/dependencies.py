from fastapi import Header, HTTPException
from src.config import API_TOKEN

def get_token_header(x_token: str = Header(...)):
    if x_token != API_TOKEN:
        raise HTTPException(status_code=403, detail="Invalid token")
