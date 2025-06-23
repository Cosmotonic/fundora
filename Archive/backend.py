# backend.py

from fastapi import FastAPI
from pydantic import BaseModel
from core import calculate_monthly_payment

app = FastAPI()

class LoanInput(BaseModel):
    principal: float
    annual_rate: float
    years: int

@app.post("/calculate")
def calculate(input: LoanInput):
    monthly = calculate_monthly_payment(input.principal, input.annual_rate, input.years)
    return {"monthly_payment": round(monthly, 2)}
