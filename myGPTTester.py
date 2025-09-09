import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class FundoraApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Fundora - Låne Evne")
        self.geometry("850x500")

        # Tabs
        tabview = ctk.CTkTabview(self)
        tabview.pack(fill="both", expand=True, padx=10, pady=10)

        tab_laan = tabview.add("Låne Evne")
        tab_bolig = tabview.add("Boligudgift")
        tab_okonomi = tabview.add("Fremtidig Økonomi")
        tab_export = tabview.add("Eksport")

        # ---------- Låne Evne Layout ----------
        # Left side
        left_frame = ctk.CTkFrame(tab_laan)
        left_frame.pack(side="left", fill="both", expand=True, padx=5, pady=5)

        self.lon1 = self.add_entry(left_frame, "Løn")
        self.pension1 = self.add_entry(left_frame, "Pension")
        self.opsparing1 = self.add_entry(left_frame, "Opsparing")
        self.gaeld1 = self.add_entry(left_frame, "Gæld")

        # Right side
        right_frame = ctk.CTkFrame(tab_laan)
        right_frame.pack(side="left", fill="both", expand=True, padx=5, pady=5)

        self.lon2 = self.add_entry(right_frame, "Løn")
        self.pension2 = self.add_entry(right_frame, "Pension")
        self.opsparing2 = self.add_entry(right_frame, "Opsparing")
        self.gaeld2 = self.add_entry(right_frame, "Gæld")

        # Results section
        result_frame = ctk.CTkFrame(tab_laan)
        result_frame.pack(fill="both", expand=True, padx=5, pady=5)

        self.samlet_indt = self.add_label(result_frame, "Samlet Indtægt")
        self.laanfaktor = self.add_label(result_frame, "Lånfaktor")
        self.lon_skat1 = self.add_label(result_frame, "Løn efter skat (1)")
        self.lon_skat2 = self.add_label(result_frame, "Løn efter skat (2)")
        self.samlet_skat = self.add_label(result_frame, "Samlet efter skat")

        # Beregn knap
        calc_btn = ctk.CTkButton(result_frame, text="Beregn", command=self.calculate)
        calc_btn.pack(pady=10)

    def add_entry(self, parent, text):
        frame = ctk.CTkFrame(parent)
        frame.pack(fill="x", pady=5)
        label = ctk.CTkLabel(frame, text=text, width=120, anchor="w")
        label.pack(side="left", padx=5)
        entry = ctk.CTkEntry(frame)
        entry.pack(side="left", fill="x", expand=True, padx=5)
        return entry

    def add_label(self, parent, text):
        frame = ctk.CTkFrame(parent)
        frame.pack(fill="x", pady=5)
        label = ctk.CTkLabel(frame, text=text, width=150, anchor="w")
        label.pack(side="left", padx=5)
        value = ctk.CTkLabel(frame, text="", anchor="w")
        value.pack(side="left", padx=5)
        return value

    def calculate(self):
        try:
            lon1 = float(self.lon1.get() or 0)
            lon2 = float(self.lon2.get() or 0)
            pension1 = float(self.pension1.get() or 0)
            pension2 = float(self.pension2.get() or 0)

            samlet = lon1 + lon2 + pension1 + pension2
            self.samlet_indt.configure(text=f"{samlet:,.0f} DKK")

            # Dummy beregninger (du kan indsætte din egen logik)
            self.laanfaktor.configure(text=f"{samlet*4:,.0f} DKK")
            self.lon_skat1.configure(text=f"{lon1*0.65:,.0f} DKK")
            self.lon_skat2.configure(text=f"{lon2*0.65:,.0f} DKK")
            self.samlet_skat.configure(text=f"{(lon1*0.65 + lon2*0.65):,.0f} DKK")

        except ValueError:
            self.samlet_indt.configure(text="Fejl i input!")

if __name__ == "__main__":
    app = FundoraApp()
    app.mainloop()
