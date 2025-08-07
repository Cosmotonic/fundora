from fpdf import FPDF
from Ctk_fundora_loanerValues import *
from tkinter import filedialog
import locale
import os

# Set locale to a European country (Danish example)
# locale.setlocale(locale.LC_ALL, 'da_DK.UTF-8')  # Use 'de_DE.UTF-8' for Germany

class FundoraPDF(FPDF):

    def footer(self):
        self.set_y(-16)
        self.set_font(TEXTFORMAT, size=8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, "Fundora - Boligværktøjet for førstegangskøbere", 0, 0, 'C')
        
class Export_finansiering_PDF(): 
    def __init__(self, set_values, mainApp, finansiering_vars, udgift_vars, fremtid_vars, eksport_vars): 

        set_values()

        self.finansiering_vars  = finansiering_vars
        self.udgift_vars        = udgift_vars
        self.fremtid_vars       = fremtid_vars
        self.eksport_vars       = eksport_vars

        # Open a file dialog 
        self.file_path = filedialog.asksaveasfilename(defaultextension=".pdf", 
                                            filetypes=[("PDF files", "*.pdf")],
                                            initialfile="Låne_Rapport",
                                            initialdir="~/Desktop")
        if not self.file_path:  
            return

        self.pdf = pdf = FundoraPDF() 
        self.pdf.set_auto_page_break(auto=True, margin=15)
        self.pdf.add_page()
        self.pdf.set_font(TEXTFORMAT, style='', size=12)

        # Title
        self.pdf.set_font(TEXTFORMAT, style='B', size=16)
        self.pdf.cell(200, 9, "Boliglånsberegner", ln=True, align="C")
    
        self.pdf.ln(5)

        # Page 
        self.bolig_information()
        self.add_personal_information()
        self.pdf.add_page()
        
        # Page 
        self.add_faste_udgifter()
        self.pdf.add_page()
    
        # Page 
        self.add_summary_section()
        self.pdf.add_page()

        # page 

        self.add_loan_section("Realkredit lån",  mainApp.fremtid_dicts['realkredit_laaneberegning'])
        self.add_loan_expectations(mainApp.fremtid_dicts['realkredit_laaneberegning'], fremtid_vars['realkredit_nominel'].get(), fremtid_vars['realkredit_terminer'].get(),
                            fremtid_vars['realkredit_laaneperiode'].get(), fremtid_vars['realkredit_bidragssats'].get())

        self.add_loan_section("Bank lån",         mainApp.fremtid_dicts['bank_laaneberegning'])
        self.add_loan_expectations(        mainApp.fremtid_dicts['bank_laaneberegning'], fremtid_vars['bank_nominel'].get(), fremtid_vars['bank_terminer'].get(),
                            fremtid_vars['bank_laaneperiode'].get())
        
        #self.AddFooter()

        # Save the PDF
        pdf.output(self.file_path)
        # self.second_page()
    
    def bolig_information(self): 
        self.pdf.set_font(TEXTFORMAT, size=12)
        self.pdf.cell(200, 9, f"Navn på boligen: {self.eksport_vars["ny_adresse_vej"].get()}", ln=True, align="W") 
        self.pdf.cell(0, 10,  "Salgsopstilling: Link (Højrekli - Åbn i ny fane)", link=self.eksport_vars["link_til_ny_adresse"].get(), align="W", ln=True) 
        self.pdf.cell(200, 9, f"Forventet Købspris: {self.udgift_vars["forventet_pris"].get()}", ln=True, align="W") 
        
    def add_personal_information(self):
        self.pdf.set_font(TEXTFORMAT, style='B', size=14)
        self.pdf.cell(200, 10, "Personlige Oplysninger", ln=True, align="L")
        self.pdf.set_font(TEXTFORMAT, size=12)

        col_widthHeader = 20  # Adjust this based on page size
        col_widthEntry = 90
        col_width = 90

        # Name
        self.pdf.cell(col_widthHeader, 10, f"Navn:", border=0)
        self.pdf.cell(col_widthEntry, 10, f"{self.eksport_vars['Fornavn1'].get()} {self.eksport_vars['Efternavn1'].get()}", border=0, align="W")
        self.pdf.cell(col_widthEntry, 10, f"{self.eksport_vars['Fornavn2'].get()} {self.eksport_vars['Efternavn2'].get()}", border=0, align="W", ln=True)

        # alder
        self.pdf.cell(col_widthHeader, 10, f"Alder:", border=0) 
        self.pdf.cell(col_widthEntry, 10, f"{self.eksport_vars['dato_dmo1'].get()}", border=0, align="W" )
        self.pdf.cell(col_widthEntry, 10, f"{self.eksport_vars['dato_dmo2'].get()}", border=0, align="W" , ln=True)

        # Vej
        self.pdf.cell(col_widthHeader, 10, f"Vej:", border=0)
        self.pdf.cell(col_widthEntry, 10, f"{self.eksport_vars['adresse_vej1'].get()}", border=0, align="W" )
        self.pdf.cell(col_widthEntry, 10, f"{self.eksport_vars['adresse_vej2'].get()}", border=0, align="W", ln=True)
        
        # Pst nr + by 
        self.pdf.cell(col_widthHeader, 10, f"By:", border=0)
        self.pdf.cell(col_widthEntry, 10, f"{self.eksport_vars['adresse_postnr1'].get()} {self.eksport_vars['adresse_by1'].get()}", border=0, align="W" ) 
        self.pdf.cell(col_widthEntry, 10, f"{self.eksport_vars['adresse_postnr2'].get()} {self.eksport_vars['adresse_by2'].get()}", border=0, align="W", ln=True)

        # Phone Number
        self.pdf.cell(col_widthHeader, 10, f"Tlf:", border=0)
        self.pdf.cell(col_widthEntry, 10, f"{self.eksport_vars['telefon1'].get()}", border=0, align="W")
        self.pdf.cell(col_widthEntry, 10, f"{self.eksport_vars['telefon2'].get()}", border=0, align="W", ln=True)

        # Email
        self.pdf.cell(col_widthHeader, 10, f"Email:", border=0)
        self.pdf.cell(col_widthEntry, 10, f"{self.eksport_vars['mail1'].get()}", border=0, align="W")
        self.pdf.cell(col_widthEntry, 10, f"{self.eksport_vars['mail2'].get()}", border=0, align="W", ln=True)

        # Løn
        self.pdf.cell(col_widthHeader, 10, f"Løn:", border=0)
        self.pdf.cell(col_widthEntry, 10, f"{locale.format_string('%.0f', float(self.finansiering_vars['indtaegt_1'].get()), grouping=True)} DKK", border=0, align="W")
        self.pdf.cell(col_widthEntry, 10, f"{locale.format_string('%.0f', float(self.finansiering_vars['indtaegt_2'].get()), grouping=True)} DKK", border=0, align="W", ln=True)

        # Løn
        self.pdf.cell(col_widthHeader, 10, f"Netto løn:", border=0)
        self.pdf.cell(col_widthEntry, 10, f"{locale.format_string('%.0f', float(self.finansiering_vars['lon_efter_skat1'].get()), grouping=True)} DKK", border=0, align="W")
        self.pdf.cell(col_widthEntry, 10, f"{locale.format_string('%.0f', float(self.finansiering_vars['lon_efter_skat2'].get()), grouping=True)} DKK", border=0, align="W", ln=True)

        # Pension
        self.pdf.cell(col_widthHeader, 10, f"Pension:", border=0)
        self.pdf.cell(col_widthEntry, 10, f"{locale.format_string('%.0f', float(self.finansiering_vars['pension_1'].get()), grouping=True)} %", border=0, align="W")
        self.pdf.cell(col_widthEntry, 10, f"{locale.format_string('%.0f', float(self.finansiering_vars['pension_2'].get()), grouping=True)} %", border=0, align="W", ln=True)

        # Opsparing
        self.pdf.cell(col_widthHeader, 10, f"Ops.:", border=0)
        self.pdf.cell(col_widthEntry, 10, f"{locale.format_string('%.0f', float(self.finansiering_vars['opsparring_1'].get()), grouping=True)} DKK", border=0, align="W")
        self.pdf.cell(col_widthEntry, 10, f"{locale.format_string('%.0f', float(self.finansiering_vars['opsparring_2'].get()), grouping=True)} DKK", border=0, align="W", ln=True)

        # Lån
        self.pdf.cell(col_widthHeader, 10, f"Gæld:", border=0)
        self.pdf.cell(col_widthEntry, 10, f"{locale.format_string('%.0f', float(self.finansiering_vars['gaeld_1'].get()), grouping=True)} DKK", border=0, align="W")
        self.pdf.cell(col_widthEntry, 10, f"{locale.format_string('%.0f', float(self.finansiering_vars['gaeld_2'].get()), grouping=True)} DKK", border=0, align="W", ln=True)

        self.pdf.ln(5)

    def add_faste_udgifter(self):
        self.pdf.set_font(TEXTFORMAT, style='B', size=14)
        self.pdf.cell(200, 10,"Faste udgifter på ny bolig", ln=True, align="L")
        self.pdf.set_font(TEXTFORMAT, size=12)

        col_width = 95  # Adjust this based on page size

        # Faste Udgifter
        self.pdf.cell(col_width, 10, f"Ejerudgift:", border=1)
        self.pdf.cell(col_width, 10, f"{self.udgift_vars['bolig_udgift'].get()} DKK", border=1, ln=True, align='R')

        self.pdf.cell(col_width, 10, f"Forbrug:", border=1)
        self.pdf.cell(col_width, 10, f"{self.udgift_vars['forbrug'].get()} DKK", border=1, ln=True, align='R')

        self.pdf.cell(col_width, 10, f"Dagligvare:", border=1)
        self.pdf.cell(col_width, 10, f"{self.udgift_vars['mad_dagligvare'].get()} DKK", border=1, ln=True, align='R')

        self.pdf.cell(col_width, 10, f"Transport:", border=1)
        self.pdf.cell(col_width, 10, f"{self.udgift_vars['transport'].get()} DKK", border=1, ln=True, align='R')

        self.pdf.cell(col_width, 10, f"Forsikring:", border=1)
        self.pdf.cell(col_width, 10, f"{self.udgift_vars['forsikringer'].get()} DKK", border=1, ln=True, align='R')

        self.pdf.cell(col_width, 10, f"Tlf, int, medie:", border=1)
        self.pdf.cell(col_width, 10, f"{self.udgift_vars['telefon_int_medie'].get()} DKK", border=1, ln=True, align='R')

        self.pdf.cell(col_width, 10, f"Personlig pleje:", border=1)
        self.pdf.cell(col_width, 10, f"{self.udgift_vars['personlig_pleje_toej'].get()} DKK", border=1, ln=True, align='R')

        self.pdf.cell(col_width, 10, f"Fritid & Fornøj:", border=1)
        self.pdf.cell(col_width, 10, f"{self.udgift_vars['fritid_fornoejelser'].get()} DKK", border=1, ln=True, align='R')

        self.pdf.cell(col_width, 10, f"Pasning & aktiviteter:", border=1)
        self.pdf.cell(col_width, 10, f"{self.udgift_vars['pasning_fritidsaktiv'].get()} DKK", border=1, ln=True, align='R')

        # Andre udgifter
        Andre_Beskrivelse1 = self.udgift_vars['flex_udgift_string1'].get()
        self.pdf.cell(col_width, 10, f"Andre udgifter: %s" % Andre_Beskrivelse1, border=1)
        self.pdf.cell(col_width, 10, f"{self.udgift_vars['flex_udgift_var1'].get()} DKK", border=1, ln=True, align='R')
        
        Andre_Beskrivelse2 = self.udgift_vars['flex_udgift_string2'].get()
        self.pdf.cell(col_width, 10, f"Andre udgifter: %s" % Andre_Beskrivelse2, border=1)
        self.pdf.cell(col_width, 10, f"{self.udgift_vars['flex_udgift_var2'].get()} DKK", border=1, ln=True, align='R')
        
        Andre_Beskrivelse3 = self.udgift_vars['flex_udgift_string3'].get()
        self.pdf.cell(col_width, 10, f"Andre udgifter: %s" % Andre_Beskrivelse3, border=1)
        self.pdf.cell(col_width, 10, f"{self.udgift_vars['flex_udgift_var3'].get()} DKK", border=1, ln=True, align='R')
        
        # Samlede udgifter
        expenses_no_loan = round(self.udgift_vars['alle_faste_udgifter'].get(),0)

        self.pdf.set_font(TEXTFORMAT, style='B', size=12)
        self.pdf.cell(col_width, 10, f"Samlede udgifter:", border=1)
        self.pdf.cell(col_width, 10, f"{expenses_no_loan} DKK", border=1, ln=True, align='R')
    
    def add_summary_section(self): 
            self.pdf.set_font(TEXTFORMAT, style='B', size=14)
            self.pdf.cell(200, 10, "Opsummering af månedlig låneydelse", ln=True, align="L")
            self.pdf.set_font(TEXTFORMAT, size=12) 

            self.pdf.cell(200, 10, f"{locale.format_string('%.0f', float(self.fremtid_vars['rente_betaling'].get()),  grouping=True)} DKK Månedelig Renter", ln=True)
            self.pdf.cell(200, 10, f"{locale.format_string('%.0f', float(self.fremtid_vars['rente_afdrag'].get() ),    grouping=True)} DKK Månedelig Afdrag", ln=True)
            self.pdf.cell(200, 10, f"{locale.format_string('%.0f', float(self.fremtid_vars['rentefradrag'].get()),   grouping=True)} DKK Månedelig Fradrag", ln=True)
            self.pdf.cell(200, 10, f"-------------", ln=True)
            self.pdf.set_font(TEXTFORMAT, style='B', size=12)
            self.pdf.cell(200, 10, f"{locale.format_string('%.0f', float(self.fremtid_vars['samlet_ydelse'].get()),    grouping=True)} DKK Ydelse", ln=True)
            self.pdf.set_font(TEXTFORMAT, size=12)
            self.pdf.cell(200, 10, f"-------------", ln=True)

            # pdf.set_font("Arial", style='B', size=12)
            self.pdf.cell(200, 10, f"{locale.format_string('%.0f', self.finansiering_vars['lon_efter_skat1'].get() + self.finansiering_vars['lon_efter_skat2'].get(), grouping=True)} DKK Løn efter skat", ln=True)
            #pdf.set_font("Arial", size=12)
            self.pdf.cell(200, 10, f"{locale.format_string('%.0f', float(self.fremtid_vars['rentefradrag'].get()), grouping=True)} DKK Rentefradrag", ln=True)
            self.pdf.cell(200, 10, f" -{locale.format_string('%.0f', self.fremtid_vars['fast_udgifter'].get(), grouping=True)} DKK Faste udgifter på ny bolig ", ln=True)
            self.pdf.cell(200, 10, f" -{locale.format_string('%.0f', float(self.fremtid_vars['samlet_ydelse'].get()), grouping=True)} DKK Ydelse for lån ", ln=True)
            self.pdf.cell(200, 10,   f"-------------", ln=True)
            self.pdf.set_font(TEXTFORMAT, style='B', size=12)

            self.pdf.cell(200, 10, f"Rådighedsbeløb: {locale.format_string('%.0f', float(self.fremtid_vars['raadighedsbeloeb'].get()), grouping=True)} DKK", ln=True)
            self.pdf.set_font(TEXTFORMAT, size=12)

            self.pdf.ln(5)
                
    def add_loan_expectations(self, loan_data, RenteSats = 0, terminer = 0, periode = 0, bidragssats = 0):
        
        if not loan_data or loan_data.get("Månedelig Cost", 0) == 0:
            print ("Månedelig Cost value ikke fundet - Kan skyldes der kun er real og ikke bank lån")

            return
        self.pdf.set_font(TEXTFORMAT, style='', size=12)
        self.pdf.cell(200, 10,   f" Rente: {RenteSats} % "
                            f" Terminer: {terminer} "
                            f" Løbetid: {periode} År "
                            f" Bidragssats: {bidragssats} % ", ln=True)
        self.pdf.ln(5)
        self.pdf.cell(200, 10, f"___________________________________________________________", ln=True)
        self.pdf.ln(5)

    def add_loan_section(self, title, loan_data):
        
        if not loan_data or loan_data.get("Månedelig Cost", 0) == 0:
            print ("Månedelig Cost value ikke fundet")

            return
            
        self.pdf.set_font(TEXTFORMAT, style='B', size=14)
        self.pdf.cell(200, 10, title, ln=True, align="L")
        self.pdf.set_font(TEXTFORMAT, size=12)

        self.pdf.cell(200, 10, f"{locale.format_string('%.0f', float(loan_data['Total Cost']), grouping=True)} DKK Total ydelse", ln=True)
        self.pdf.cell(200, 10, f"{locale.format_string('%.0f', float(loan_data['Total Interest']), grouping=True)} DKK Total Rente", ln=True)
        self.pdf.cell(200, 10, f"{locale.format_string('%.0f', float(loan_data['Rentefradrag']), grouping=True)} DKK Total Rentefradrag", ln=True)

        self.pdf.ln(5)

        # Add first 3 payments
        self.pdf.set_font(TEXTFORMAT, style='B', size=12)
        self.pdf.cell(200, 10, "Første 4 hele Terminer i amortisationsplan:", ln=True)
        self.pdf.set_font(TEXTFORMAT, size=10)

        for i, payment in enumerate(loan_data["Amortization Schedule"][:4], start=1): #[:3]
            self.pdf.cell(200, 10, f"Period {i}: Ydelse: {payment['Ydelse']:.0f} DKK, "
                                f"Rente: {payment['Rente']:.0f} DKK, "
                                f"Afdrag: {payment['Afdrag']:.0f} DKK, "
                                f"Restgæld: {payment['Restgæld']:.0f} DKK", ln=True)
        self.pdf.ln(5)          


class Eksport_rennovation_budget_PDF:
    def __init__(self, data_dict, renovation_vars):
        
        if not data_dict:
            return

        print (data_dict)

        file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
            initialfile=renovation_vars['budget_titel'],
            initialdir=os.path.expanduser("~/Desktop")
        )

        if not file_path:
            return

        self.pdf = FundoraPDF()
        # Lav første side
        self.pdf.set_auto_page_break(auto=True, margin=15)
        self.pdf.add_page()
        self.pdf.set_font("Helvetica", style='B', size=16)
        self.pdf.cell(200, 10, renovation_vars['budget_titel'].get(), ln=True, align="C")
        self.pdf.ln(5)

        self.tilføj_kontakt_info(renovation_vars)

        self.pdf.set_font("Helvetica", size=12)
        total_price = 0

        # Beskrivelse i rækkefølge: 
        headers = [" ", "Kommentar", "Tid", "Prio", "Pris"]
        self.col_widths = [40, 70, 30, 25, 25]

        for header, width in zip(headers, self.col_widths):
            self.pdf.cell(width, 8, header, border=0)
        self.pdf.ln()


        for reno_id, reno_data in data_dict.items():
            if not reno_data.get("inkluder_i_budget", True):
                continue

            opgaver = reno_data.get("opgaver", {})
            if not opgaver:
                continue
            
            Reno_navn = reno_data.get('hovedoppgave_navn')
            print (f'Renovations navn: {Reno_navn}')
            if not Reno_navn: 
                continue

            self.tilføj_renovation_sektion(reno_id, opgaver, renovation_Navn=Reno_navn)
            total_price += self.sum_renovation(opgaver)

        # Samlet total højrejusteret
        self.pdf.set_font("Helvetica", style='B', size=12)
        self.pdf.cell(0, 10, f"Samlet totalpris: {total_price:,.0f} DKK", ln=True, align="R")
        self.pdf.output(file_path)
        print("PDF gemt som:", file_path)
        if os.path.exists(file_path):
            os.startfile(file_path)

    def tilføj_kontakt_info(self, kontakt_dict):
        self.pdf.set_font("Helvetica", size=11)
        self.pdf.ln(2)  # lidt afstand fra titlen

        kontaktfelter = {
            "Kontaktperson": kontakt_dict['kontakt_navn'].get(),
            "Telefon": kontakt_dict['kontakt_telefon'].get(),
            "Email": kontakt_dict['kontakt_mail'].get()
        }

        for label, value in kontaktfelter.items():
            self.pdf.cell(30, 8, f"{label}:", border=0)
            self.pdf.cell(100, 8, value, border=0, ln=True)

        self.pdf.ln(5)  # lidt ekstra luft bagefter




    def tilføj_renovation_sektion(self, reno_id, opgaver, renovation_Navn):
        self.pdf.set_font("Helvetica", style='B', size=14)
        self.pdf.cell(200, 10, f"{renovation_Navn}", ln=True)
        self.pdf.set_font("Helvetica", style='', size=11)

        for opgavenavn, opgavedata in opgaver.items():
            if opgavedata.get("ekskludere", False):
                continue

            values = [
                opgavedata.get("Opgave", opgavenavn),
                opgavedata.get("Kommentar/Blokkere", ""),
                opgavedata.get("Tidsforbrug", ""),
                opgavedata.get("Prio", ""),
                opgavedata.get("Pris", "0")
            ]

            for val, width in zip(values, self.col_widths):
                self.pdf.cell(width, 8, str(val), border=0)
            self.pdf.ln()
        self.pdf.ln(5)

    def sum_renovation(self, opgaver):
        total = 0
        for opgavedata in opgaver.values():
            if opgavedata.get("ekskludere", False):
                continue
            pris_str = opgavedata.get("Pris", "0").strip()
            try:
                pris = float(pris_str.replace(".", "").replace(",", "."))
                total += pris
            except ValueError:
                pass
        return total



class FundoraPDF(FPDF):
    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", size=8)
        self.cell(0, 10, "Fundora - Din boligforhandler", align="C")



class Eksport_forhandling_PDF:
    def __init__(self, data_vars, forhandlings_arg_løs): 
        if not forhandlings_arg_løs:
            return

        print (forhandlings_arg_løs)

        file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
            initialfile=data_vars['forhandling_titel'],
            initialdir=os.path.expanduser("~/Desktop")
        )

        if not file_path:
            return

        self.pdf = FundoraPDF()
        self.pdf.set_auto_page_break(auto=True, margin=15)
        self.pdf.add_page()

        # Titel
        self.pdf.set_font("Helvetica", style='B', size=16)
        self.pdf.cell(200, 10, data_vars['forhandling_titel'].get(), ln=True, align="C")
        self.pdf.ln(5)

        self.pdf.set_font("Helvetica", size=12)

        # Strategi
        strategi_tekst = self.lav_forhandlings_strategi_tekst(data_vars)
        self.tilføj_afsnit("forhandlingsstrategi", strategi_tekst)

        # Argumenter tabel
        #print (f"Argumenter: {forhandlings_arg_løs["argumenter"]}")
        self.pdf.add_page()
        self.tilføj_tabel("Argumenter", forhandlings_arg_løs["argumenter"])

        # Løsøre tabel
        #print (f"Løsøre: {forhandlings_arg_løs["argumenter"]}")
        self.pdf.add_page()
        self.tilføj_tabel("Løsøre", forhandlings_arg_løs["losore"])

        # Gem PDF
        self.pdf.output(file_path)
        #print("PDF gemt som:", file_path)
        if os.path.exists(file_path):
            os.startfile(file_path)

    def lav_forhandlings_strategi_tekst(self, data_vars):
        udbudspris     = data_vars["udbudspris"].get()
        afslagsprocent = data_vars["forventet_procent"].get()
        maxpris        = data_vars["forventet_pris"].get()
        aggressivitet  = data_vars["aggressivitet"].get()

        tekst =  f"Udbudspris: {udbudspris} kr.\n"
        tekst += f"Forventet afslag (%): {afslagsprocent}%\n"
        tekst += f"Maks købspris: {maxpris} kr.\n"
        tekst += f"Aggressivitet (slider): {aggressivitet}\n\n"

        for i in range(1, 5):
            procent = data_vars[f"runde{i}_procent"].get()
            pris    = data_vars[f"runde{i}_pris"].get()
            tekst += f"{i}. Bud: {procent}% -> {pris} kr.\n"

        return tekst    



    def tilføj_afsnit(self, overskrift, tekst):
        self.pdf.set_font("Helvetica", style='B', size=14)
        self.pdf.cell(200, 10, overskrift, ln=True)
        self.pdf.set_font("Helvetica", size=12)
        self.pdf.multi_cell(0, 10, tekst)
        self.pdf.ln(5)

    def tilføj_tabel(self, titel, data_dict):
        if not data_dict:
            return

        self.pdf.set_font("Helvetica", style='B', size=14)
        self.pdf.cell(200, 10, titel, ln=True)
        self.pdf.ln(2)

        # Header
        self.pdf.set_font("Helvetica", style='B', size=12)
        self.pdf.cell(60, 10, "Punkt", 1)
        self.pdf.cell(30, 10, "Prioritet", 1)
        self.pdf.cell(100, 10, "Kommentar", 1)
        self.pdf.ln()

        # Rows
        self.pdf.set_font("Helvetica", size=12)
        for punkt, data in data_dict.items():
            #print (f"challenge area: {data.get('checked')}")
            if data.get("checked") == True: 
                prioritet = data.get("priority", "")
                kommentar = data.get("comment", "")
                label = data.get("label", "")

                self.pdf.cell(60, 10, label, 1)
                self.pdf.cell(30, 10, prioritet, 1)
                self.pdf.cell(100, 10, kommentar, 1)
                self.pdf.ln()

        self.pdf.ln(5)




