# ui.py

import customtkinter as ctk
import requests

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Fundora Login")
app.geometry("400x450")

email_entry = ctk.CTkEntry(app, placeholder_text="Email")
email_entry.pack(pady=10)

password_entry = ctk.CTkEntry(app, placeholder_text="Password", show="*")
password_entry.pack(pady=10)

result_label = ctk.CTkLabel(app, text="")
result_label.pack(pady=20)

def try_login():
    payload = {
        "email": email_entry.get(),
        "password": password_entry.get()
    }
    try:
        res = requests.post("http://127.0.0.1:8000/login", json=payload)
        data = res.json()
        if data["status"] == "success":
            user = data["user"]
            result_label.configure(text=f"Welcome, {user['name']}!\nAddress: {user['address']}, \nPhone: {user['phone']}, \nAge: {user['age']}")
        else:
            result_label.configure(text="Login failed.")
    except Exception as e:
        result_label.configure(text=f"Error: {e}")

login_button = ctk.CTkButton(app, text="Login", command=try_login)
login_button.pack(pady=10)

app.mainloop()
