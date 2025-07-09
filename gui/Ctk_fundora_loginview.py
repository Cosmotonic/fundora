import customtkinter as ctk
from database.Ctk_fundora_auth import login_user, register_user
import mysql.connector



class LoginFrame(ctk.CTkFrame):
    def __init__(self, master, on_success):
        super().__init__(master)
        self.master = master
        self.on_success = on_success

        self.label = ctk.CTkLabel(self, text="LOG IND I FUNDORA", font=("Helvetica", 18, "bold"))
        self.label.pack(pady=20)

        self.email_var = ctk.StringVar(value="kasper@voca.com")
        self.email_entry = ctk.CTkEntry(self, placeholder_text="emial", textvariable=self.email_var, width=300)
        self.email_entry.pack(pady=10)

        self.pass_var = ctk.StringVar(value="mitKodeord123")
        self.password_entry = ctk.CTkEntry(self, placeholder_text="password", show="*", textvariable=self.pass_var, width=300)
        self.password_entry.pack(pady=10)

        self.login_button = ctk.CTkButton(self, text="Login", command=self.try_login)
        self.login_button.pack(pady=10)

        self.register_button = ctk.CTkButton(self, text="Opret ny bruger", command=self.try_register, 
                                           hover_color="#EC6E07", 
                                           fg_color='transparent', 
                                           border_color="#FF9100", )
        self.register_button.pack(pady=5)

        self.status_label = ctk.CTkLabel(self, text="", text_color="red")
        self.status_label.pack(pady=5)

    def try_login(self):
        email = self.email_entry.get()
        password = self.password_entry.get()
        if login_user(email, password):
            self.status_label.configure(text="Login succesfuldt!", text_color="green")
            self.on_success(email)
        else:
            self.status_label.configure(text="Forkert loginoplysning", text_color="red")

    def try_register(self):
        email = self.email_entry.get()
        password = self.password_entry.get()
        if email and password:
            register_user(email, password)
            self.status_label.configure(text="Bruger oprettet – prøv at logge ind", text_color="green")
        else:
            self.status_label.configure(text="Udfyld email og adgangskode", text_color="red")
