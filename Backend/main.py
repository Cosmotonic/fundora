# main.py
from fastapi import FastAPI
from pydantic import BaseModel
from fundora_core import calculate_monthly_payment

app = FastAPI()


class PrintInput(BaseModel): 
    printstatement: float

@app.post("/printer")
def printer(input: PrintInput): 
    print (input.printstatement) # only works in server. 
    sentence = f"Here is the number buddy {input.printstatement}" 
    return (sentence) # works on json too. 
    
    
    
'''
class LoanInput(BaseModel):
    principal: float
    annual_rate: float
    years: int

@app.post("/calculate")
def calculate(input: LoanInput):
    monthly = calculate_monthly_payment(input.principal, input.annual_rate, input.years)
    return {
        "monthly_payment": round(monthly, 2),
        "total_paid": round(monthly * input.years * 12, 2)
    }

'''