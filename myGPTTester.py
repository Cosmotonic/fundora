import customtkinter as ctk
from transformers import pipeline

# Setup
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

# Load GPT-2 model (lokalt)
generator = pipeline("text-generation", model="gpt2")

# GPT-generering
def generate_ai_argument(user_input, perspective):
    # Dansk til engelsk intro
    if perspective == "Fordel":
        intro = "We believe the long time on market is an opportunity because"
    else:
        intro = "We are cautious about the short time on market because"

    # Sæt prompt sammen
    prompt = f"{intro} {user_input}. Therefore, we think that"

    # Generér svar
    result = generator(prompt, max_length=80, num_return_sequences=1)
    return result[0]["generated_text"]

# GUI-app
class ArgumentGeneratorApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Fundora – Offline AI Forhandlingsgenerator (GPT-2)")
        self.geometry("800x500")

        ctk.CTkLabel(self, text="Argument: Liggetid", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=(20, 5))

        self.perspective_option = ctk.CTkOptionMenu(self, values=["Fordel", "Ulempe"])
        self.perspective_option.set("Fordel")
        self.perspective_option.pack(pady=(0, 10))

        ctk.CTkLabel(self, text="Skriv din begrundelse på dansk (bliver kombineret med engelsk intro):").pack()
        self.input_box = ctk.CTkTextbox(self, height=100, width=600)
        self.input_box.pack(pady=5)

        self.generate_button = ctk.CTkButton(self, text="Generer AI-svar", command=self.on_generate)
        self.generate_button.pack(pady=10)

        self.output_label = ctk.CTkLabel(self, text="AI-genereret (engelsk) svar vises her...", wraplength=700, justify="left")
        self.output_label.pack(padx=20, pady=20)

    def on_generate(self):
        user_input = self.input_box.get("1.0", "end").strip()
        perspective = self.perspective_option.get()

        if not user_input:
            self.output_label.configure(text="❌ Skriv venligst din begrundelse.")
            return

        self.output_label.configure(text="⏳ Genererer svar...")
        self.update_idletasks()

        result = generate_ai_argument(user_input, perspective)
        self.output_label.configure(text=result)

if __name__ == "__main__":
    app = ArgumentGeneratorApp()
    app.mainloop()
