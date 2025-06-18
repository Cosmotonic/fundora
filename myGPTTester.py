import customtkinter as ctk
from tkinter import messagebox

# Brugerdatabase (kan være fra en fil eller database senere)
brugere = {
    "kasper": "1234",
    "franzi": "qwerty",
    "test": "letmein"
}

class LoginApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Login")
        self.geometry("300x200")

        ctk.CTkLabel(self, text="Brugernavn").pack(pady=(20, 5))
        self.entry_user = ctk.CTkEntry(self)
        self.entry_user.pack()

        ctk.CTkLabel(self, text="Adgangskode").pack(pady=(10, 5))
        self.entry_pass = ctk.CTkEntry(self, show="*")
        self.entry_pass.pack()

        ctk.CTkButton(self, text="Login", command=self.tjek_login).pack(pady=20)

    def tjek_login(self):
        bruger = self.entry_user.get()
        kode = self.entry_pass.get()

        if bruger in brugere and brugere[bruger] == kode:
            messagebox.showinfo("Login", f"Velkommen, {bruger}!")
            self.destroy()  # luk login-vinduet
            MainApp()  # åbn hovedprogram
        else:
            messagebox.showerror("Fejl", "Forkert brugernavn eller adgangskode.")

class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Hovedprogram")
        self.geometry("400x300")
        ctk.CTkLabel(self, text="Du er nu logget ind!").pack(pady=40)
        self.mainloop()

if __name__ == "__main__":
    ctk.set_appearance_mode("light")
    app = LoginApp()
    app.mainloop()
