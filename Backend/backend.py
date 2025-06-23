# backend.py

from fastapi import FastAPI
from pydantic import BaseModel
from Archive.core import verify_user

app = FastAPI()

class LoginInput(BaseModel):
    email: str
    password: str

@app.post("/login")
def login(data: LoginInput):
    user = verify_user(data.email, data.password)
    if user:
        return {"status": "success", "user": user}
    return {"status": "error", "message": "Invalid credentials"}
