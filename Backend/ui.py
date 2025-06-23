# ui.py

import customtkinter as ctk
import requests

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Loan Calculator")
app.geometry("400x300")

entry_principal = ctk.CTkEntry(app, placeholder_text="Loan Amount")
entry_principal.pack(pady=10)

entry_rate = ctk.CTkEntry(app, placeholder_text="Interest Rate (%)")
entry_rate.pack(pady=10)

entry_years = ctk.CTkEntry(app, placeholder_text="Loan Term (Years)")
entry_years.pack(pady=10)

result_label = ctk.CTkLabel(app, text="Result will appear here")
result_label.pack(pady=20)

def call_backend():
    try:
        payload = {
            "principal": float(entry_principal.get()),
            "annual_rate": float(entry_rate.get()),
            "years": int(entry_years.get())
        }
        res = requests.post("http://127.0.0.1:8000/calculate", json=payload)
        data = res.json()
        result_label.configure(text=f"Monthly: {data['monthly_payment']:.2f} DKK")
    except Exception as e:
        result_label.configure(text=f"Error: {e}")

btn = ctk.CTkButton(app, text="Calculate", command=call_backend)
btn.pack(pady=10)

app.mainloop()
