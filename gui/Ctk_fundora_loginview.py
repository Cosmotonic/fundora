import customtkinter as ctk
from database.Ctk_fundora_auth import login_user, register_user
import mysql.connector
from Ctk_fundora_loanerValues import *


class Login_Center(ctk.CTkFrame):
    def __init__(self, master, on_success):
        super().__init__(master)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.on_success = on_success

        # Sidebar
        self.sidebar = ctk.CTkFrame(self, width=300, fg_color=ORANGE)
        self.sidebar.grid(row=0, column=0, sticky="ns")
        self.sidebar.grid_rowconfigure((0,1,2,3), weight=1)
        self.sidebar.grid_columnconfigure(0, weight=1)

        self.login_btn      = ctk.CTkButton(self.sidebar, text="Login", command=self.show_login, hover_color=HIGHTLIGHT_ORANGE, text_color=DARK_TEXT_COLOR, fg_color=WHITE, corner_radius=20, font=ctk.CTkFont(weight="bold"))
        self.login_btn.grid(row=1, column=0, pady=(20,20), padx=40, sticky="sew")

        self.register_btn   = ctk.CTkButton(self.sidebar, text="Register", command=self.show_register, hover_color=HIGHTLIGHT_ORANGE, text_color=WHITE_TEXT_COLOR, fg_color=DARK_ORANGE, corner_radius=20)
        self.register_btn.grid(row=2, column=0, pady=(20,20), padx=40, sticky="new")

        # Content
        self.content_frame = ctk.CTkFrame(self, fg_color=WHITE)
        self.content_frame.grid(row=0, column=1, sticky="nsew")
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(0, weight=1)

        self.login_view = LoginFrame(self.content_frame, self.on_success, self.show_register)
        self.register_view = RegisterFrame(self.content_frame, self.on_success, self.show_login)

        self.login_view.grid(row=0, column=0, sticky="nsew")

    def show_login(self):
        self.register_view.grid_forget()
        self.login_view.grid(row=0, column=0, sticky="nsew")
        self.login_btn.configure(fg_color=WHITE, text_color=DARK_TEXT_COLOR)
        self.register_btn.configure(fg_color=DARK_ORANGE, text_color=WHITE_TEXT_COLOR)


    def show_register(self):
        self.login_view.grid_forget()
        self.register_view.grid(row=0, column=0, sticky="nsew")
        self.login_btn.configure(fg_color=DARK_ORANGE, text_color=WHITE_TEXT_COLOR)
        self.register_btn.configure(fg_color=WHITE, text_color=DARK_TEXT_COLOR)


class LoginFrame(ctk.CTkFrame):
    def __init__(self, master, on_success, switch_to_register):
        super().__init__(master, fg_color=WHITE)
        self.grid_columnconfigure((0,1,2), weight=1)
        self.grid_rowconfigure((0,1,2), weight=1)

        centerFrame = ctk.CTkFrame(self, fg_color="transparent")
        centerFrame.grid(row=1, column=1, columnspan=1)# 
        centerFrame.grid_columnconfigure(0, weight=1)

        self.on_success = on_success

        headline = ctk.CTkLabel(centerFrame, text="LOGIN I FUNDORA", font=("poppins", 30, "bold"))
        headline.grid(row=0, column=0, pady=(40, 10))

        self.email_var = ctk.StringVar(value="kasper@voca.com")
        self.email_entry = ctk.CTkEntry(centerFrame, placeholder_text="NAVN", textvariable=self.email_var, corner_radius=20)
        self.email_entry.grid(row=1, column=0, pady=5, padx=40, sticky="ew")

        self.pass_var = ctk.StringVar(value="mitKodeord123")
        self.password_entry = ctk.CTkEntry(centerFrame, placeholder_text="PASSWORD", textvariable=self.pass_var, show="*", corner_radius=20)
        self.password_entry.grid(row=2, column=0, pady=5, padx=40, sticky="ew")

        self.status_label = ctk.CTkLabel(centerFrame, text="", text_color="red")
        self.status_label.grid(row=3, column=0, pady=(0, 5))

        self.login_But = ctk.CTkButton(centerFrame, text="Login", fg_color=PURPLE, hover_color=LIGHT_PURPLE, command=self.try_login, corner_radius=20, font=ctk.CTkFont(weight="bold"))
        self.login_But.grid(row=4, column=0, pady=(20, 5), padx=40)

        self.to_register = ctk.CTkButton(centerFrame, text="Registrer ny bruger", fg_color="transparent", command=switch_to_register, text_color="black", font=ctk.CTkFont(size=12), hover=False)
        self.to_register.grid(row=5, column=0, pady=(0, 10))

        self.glemt_password_but = ctk.CTkButton(centerFrame, text="Glemt password?", fg_color="transparent", text_color="black", font=ctk.CTkFont(size=12), hover=False)
        self.glemt_password_but.grid(row=6, column=0, sticky="se", padx=10, pady=(10, 10))

    def try_login(self):
        email = self.email_entry.get()
        password = self.password_entry.get()
        if login_user(email, password):
            self.status_label.configure(text="Login succesfuldt!", text_color="green")
            self.on_success(email)
        else:
            self.status_label.configure(text="Forkert loginoplysning", text_color="red")


class RegisterFrame(ctk.CTkFrame):
    def __init__(self, master, on_success, switch_to_login):
        super().__init__(master, fg_color=WHITE)

        self.grid_columnconfigure((0,1,2), weight=1)
        self.grid_rowconfigure((0,1,2), weight=1)

        centerFrame = ctk.CTkFrame(self, fg_color="transparent")
        centerFrame.grid(row=1, column=1, columnspan=1, sticky="ew")# 
        centerFrame.grid_columnconfigure(0, weight=1)

        self.on_success = on_success

        header1 = ctk.CTkLabel(centerFrame, text="OPRET NY BRUGER", font=("Helvetica", 22, "bold"))
        header1.grid(row=0, column=0, pady=(30, 10))

        self.navn_entry = ctk.CTkEntry(centerFrame, placeholder_text="NAVN", corner_radius=20)
        self.navn_entry.grid(row=1, column=0, pady=5, padx=40, sticky="ew")

        self.telefon_entry = ctk.CTkEntry(centerFrame, placeholder_text="TELEFON", corner_radius=20)
        self.telefon_entry.grid(row=2, column=0, pady=5, padx=40, sticky="ew")

        self.email_entry = ctk.CTkEntry(centerFrame, placeholder_text="EMAIL", corner_radius=20)
        self.email_entry.grid(row=3, column=0, pady=5, padx=40, sticky="ew")

        self.koen_combobox = ctk.CTkComboBox(
            master=centerFrame,
            values=["Kvinde", "Mand", "Andet"],
            corner_radius=10,
            width=180,
            fg_color="white",  # baggrundsfarve for tekstfeltet
            text_color="black",  # tekst i feltet
            border_color=PURPLE,
            border_width=2,
            font=("Helvetica", 14),  # bruger font i feltet
            dropdown_fg_color="#FFFFFF",  # baggrund i dropdown
            dropdown_text_color="black",  # tekst i dropdown
        )
        self.koen_combobox.set("Vælg køn")  # standardtekst
        self.koen_combobox.grid(row=4, column=0, pady=5, padx=40, sticky="ew")
        
        self.password_entry = ctk.CTkEntry(centerFrame, placeholder_text="Password", show="*", corner_radius=20)
        self.password_entry.grid(row=5, column=0, pady=5, padx=40, sticky="ew")

        self.password_gentag_entry = ctk.CTkEntry(centerFrame, placeholder_text="Gentag Password", show="*", corner_radius=20)
        self.password_gentag_entry.grid(row=6, column=0, pady=5, padx=40, sticky="ew")

        self.check_personlig_data = ctk.CTkCheckBox(centerFrame, text="Tilladelse om adgang til personlige data")
        self.check_personlig_data.grid(row=7, column=0, pady=(10, 2), padx=40, sticky="w")
        
        self.check_kontakt = ctk.CTkCheckBox(centerFrame, text="Tilladelse til at blive kontaktet")
        self.check_kontakt.grid(row=8, column=0, pady=(0, 10), padx=40, sticky="w")

        self.status_label = ctk.CTkLabel(centerFrame, text="Eventuelle fejl beskeder", text_color="red")
        self.status_label.grid(row=9, column=0, pady=(0, 5))

        self.register_button = ctk.CTkButton(centerFrame, text="Registrer", fg_color=PURPLE, hover_color=LIGHT_PURPLE, corner_radius=30, font=ctk.CTkFont(weight="bold"))
        self.register_button.grid(row=10, column=0, pady=10, padx=40, sticky="ew")

        self.tilbage_button = ctk.CTkButton(centerFrame, text="Tilbage til login", command=switch_to_login, fg_color="transparent", text_color="black", hover=False)
        self.tilbage_button.grid(row=11, column=0, pady=(0, 20))

    def try_register(self):
        email = self.email_entry.get()
        password = self.password_entry.get()
        if email and password:
            register_user(email, password)
            self.status_label.configure(text="Bruger oprettet – prøv at logge ind", text_color="green")
        else:
            self.status_label.configure(text="Udfyld email og adgangskode", text_color="red")

