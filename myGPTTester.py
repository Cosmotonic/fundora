
import customtkinter as ctk

# Farver i dit UI
ORANGE = "#FEB07D"
DARK_ORANGE = "#D18050"
LIGHT_ORANGE ="#F8A969"
PURPLE = "#6843A9"
LIGHT_PURPLE = "#8E65D4"
HOVER_PURPLE = "#AD8FE2"

WHITE = "#FFFFFF"

class LoginFrame(ctk.CTkFrame):
    def __init__(self, master, switch_to_register):
        super().__init__(master, fg_color=WHITE)
        self.grid_columnconfigure((0,1,2,3,4), weight=1)

        ctk.CTkLabel(self, text="LOGIN I FUNDORA", font=("Helvetica", 22, "bold")).grid(row=0, column=2, pady=(40, 10))

        self.name_entry = ctk.CTkEntry(self, placeholder_text="NAVN", corner_radius=20)
        self.name_entry.grid(row=1, column=2, pady=5, padx=40, sticky="ew")

        self.password_entry = ctk.CTkEntry(self, placeholder_text="PASSWORD", show="*", corner_radius=20)
        self.password_entry.grid(row=2, column=2, pady=5, padx=40, sticky="ew")

        ctk.CTkButton(self, text="Login", fg_color=PURPLE, hover_color=LIGHT_PURPLE, corner_radius=20, font=ctk.CTkFont(weight="bold")).grid(row=3, column=2, pady=(20, 5), padx=40)

        ctk.CTkLabel(self, text="Registrer ny bruger", font=ctk.CTkFont(size=12)).grid(row=4, column=2, pady=(5, 40))

        ctk.CTkButton(self, text="Glemt password?", fg_color="transparent", text_color="black", font=ctk.CTkFont(size=12), hover=False).grid(row=5, column=2, sticky="se", padx=10, pady=(10, 10))


class RegisterFrame(ctk.CTkFrame):
    def __init__(self, master, switch_to_login):
        super().__init__(master, fg_color=WHITE)
        self.grid_columnconfigure((0,1,2,3,4), weight=1)

        ctk.CTkLabel(self, text="OPRET NY BRUGER", font=("Helvetica", 22, "bold")).grid(row=0, column=2, pady=(30, 10))

        entries = [
            ("NAVN", 1),
            ("TELEFON", 2),
            ("EMAIL", 3)
        ]
        for text, r in entries:
            ctk.CTkEntry(self, placeholder_text=text, corner_radius=20).grid(row=r, column=2, pady=5, padx=40, sticky="ew")

        '''
        combo = ctk.CTkComboBox(
            master=self,
            values=["Mand", "Kvinde", "Andet"],
            width=180,
            corner_radius=10,
            fg_color=PURPLE,         # field background
            border_color="#741E7F",
            text_color="white",
            dropdown_fg_color="#FFFFFF",
            dropdown_text_color="black",
            dropdown_font=("helvita", 14),
            dropdown_hover_color=LIGHT_PURPLE,
            justify="center", 
            #dropdown_border_color = "#00C241",
            button_color=PURPLE,
            button_hover_color=LIGHT_PURPLE,
        )
        combo.set("Vælg Køn")  # default value
        combo.grid(row=4, column=2, padx=10, pady=10)

        print (combo.get())
        '''
        
        #ctk.CTkOptionMenu(self, values=["Kvinde", "Mand", "Andet"], corner_radius=20).grid(row=4, column=2, pady=5, padx=40, sticky="ew")
        menu = ctk.CTkOptionMenu(
            self,
            values=["Skal gøres", "Bør gøres", "Kan gøres"],
            corner_radius=10,
            fg_color=PURPLE,          # knapbaggrund
            button_color=PURPLE,      # dropdown pilens baggrund
            button_hover_color=LIGHT_PURPLE, # hover på pil
            text_color="white",          # tekst
            dropdown_fg_color="#FFFFFF", # dropdown baggrund
            dropdown_hover_color=HOVER_PURPLE,
            dropdown_text_color="black",  # tekst i dropdown
            dropdown_font=("helvita", 14),
            width=180,
            )
        menu.grid(row=4, column=2, pady=5, padx=40)
        menu.set("             Vælg køn")

        ctk.CTkEntry(self, placeholder_text="Password", show="*", corner_radius=20).grid(row=5, column=2, pady=5, padx=40, sticky="ew")
        ctk.CTkEntry(self, placeholder_text="Gentag Password", show="*", corner_radius=20).grid(row=6, column=2, pady=5, padx=40, sticky="ew")

        ctk.CTkCheckBox(self, text="Tilladelse om adgang til personlige data").grid(row=7, column=2, pady=(10, 2), padx=40, sticky="w")
        ctk.CTkCheckBox(self, text="Tilladelse til at blive kontaktet").grid(row=8, column=2, pady=(0, 10), padx=40, sticky="w")

        ctk.CTkLabel(self, text="Eventuelle fejl beskeder", text_color="red").grid(row=9, column=2, pady=(0, 5))

        ctk.CTkButton(self, text="Registrer", fg_color=PURPLE, hover_color=LIGHT_PURPLE, corner_radius=30, font=ctk.CTkFont(weight="bold")).grid(row=10, column=2, pady=10, padx=40, sticky="ew")

        ctk.CTkButton(self, text="Tilbage til login", command=switch_to_login, fg_color="transparent", text_color=PURPLE).grid(row=11, column=2, pady=(0, 20))


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1100x700")
        self.title("Fundora Login/Register UI")
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        
        # Sidebar
        self.sidebar = ctk.CTkFrame(self, width=300, fg_color=ORANGE)
        self.sidebar.grid(row=0, column=0, sticky="ns")
        self.sidebar.grid_rowconfigure((0,1,2,3), weight=1)
        self.sidebar.grid_columnconfigure(0, weight=1)

        self.login_btn = ctk.CTkButton(self.sidebar, text="Login", command=self.show_login, fg_color=DARK_ORANGE, corner_radius=20, font=ctk.CTkFont(weight="bold"))
        self.login_btn.grid(row=1, column=0, pady=(20,20), padx=40, sticky="sew")

        self.register_btn = ctk.CTkButton(self.sidebar, text="Register", command=self.show_register, fg_color=WHITE, text_color="black", corner_radius=20)
        self.register_btn.grid(row=2, column=0, pady=(20,20), padx=40, sticky="new")

        # Content
        self.content_frame = ctk.CTkFrame(self, fg_color=WHITE)
        self.content_frame.grid(row=0, column=1, sticky="nsew")
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(0, weight=1)

        self.login_view = LoginFrame(self.content_frame, self.show_register)
        self.register_view = RegisterFrame(self.content_frame, self.show_login)

        self.login_view.grid(row=0, column=0, sticky="nsew")

    def show_login(self):
        self.register_view.grid_forget()
        self.login_view.grid(row=0, column=0, sticky="nsew")

    def show_register(self):
        self.login_view.grid_forget()
        self.register_view.grid(row=0, column=0, sticky="nsew")


if __name__ == "__main__":
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")
    app = App()
    app.mainloop()


