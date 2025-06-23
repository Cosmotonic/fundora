# fundora_core.py

def calculate_monthly_payment(principal, annual_rate, years):
    rate = annual_rate / 100 / 12
    months = years * 12
    if rate == 0:
        return principal / months
    return principal * rate / (1 - (1 + rate) ** -months)
