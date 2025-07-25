# Lav ny Class hver gang den skal kaldes fra main scriptet. Image_output Image_Import
# brug alle udnerfoldere 
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), ".")))

import atexit

import customtkinter as ctk
import backend.Ctk_fundora_exportPDF as export 
import backend.Ctk_fundora_math_lib as fuMath 
import database.Fundora_data_handler as dbhandler

from Ctk_fundora_loanerValues import *
from gui.Ctk_fundora_hubview import * 
from gui.Ctk_fundora_forhandling import * 
from gui.Ctk_fundora_finansiering import * 
from gui.Ctk_fundora_renovering import * 
from gui.Ctk_fundora_loginview import Login_Center
from components.Ctk_fundora_panels import *



class App(ctk.CTk): 
    def __init__(self):
        super().__init__()
        self.current_view = None
        ctk.set_appearance_mode('light')
        self.geometry('1280x720')
        self.appVersion = "0.2"

        self.title(f'Fundora v.{self.appVersion}')

        self.minsize(800,500)

        # set all parameters. 
        self.factory_parameter_settings()

        # Start med login view
        self.logged_in = False
        self.show_login_view()

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Gem i tilfælde af lukning
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        # start program
        self.mainloop()

    def show_login_view(self):
        if self.current_view:
            self.current_view.destroy()

        self.current_view = Login_Center(self, self.on_login_success)
        self.current_view.grid(row=0, column=0, sticky="nsew")

    def on_login_success(self, email):
        self.logged_in_email = email
        self.to_hubview()  # Når login er korrekt
        self.factory_parameter_settings() # Reset to default config params, before pulling db info
        self.importer_data_fra_db() # automatically load data from cb based on logged in email
        self.logged_in = False

    def to_hubview(self):
        self.current_view.destroy()
        self.hubview = hubview(self, logout_callback=self.back_to_login_screen, finansiering = self.menu_finansierng, forhandling = self.menu_forhandling, budgetværktøj = self.menu_budgetvaerktoej)  # 
        self.current_view = self.hubview
        
        # Only trace needed values. Or use all:  combined_vars = list(self.forhandlings_vars.values()) 
        self.combined = [self.forhandlings_vars['aggressivitet'], self.forhandlings_vars['forventet_pris'], self.forhandlings_vars['forventet_procent']]
        for var in self.combined:
            var.trace('w', self.manipulate_forhandling)

    def factory_parameter_settings(self):
        self.init_Finansiering_parameters()
        self.init_Forhandling_parameters()
        self.init_udgift_parameters()
        self.init_fremtid_parameters()
        self.init_person_info_parameters()
        self.init_budgetvaerktoej_parameters()
        self.init_UGC_parameters()

    def init_Finansiering_parameters(self): 
        self.finansiering_vars = {
            "indtaegt_1"        : ctk.DoubleVar(value=PERSON1_LOEN),              
            "pension_1"         : ctk.DoubleVar(value=PERSON1_PENSION), 
            "opsparring_1"      : ctk.DoubleVar(value=PERSON1_SAVINGS),
            "gaeld_1"           : ctk.DoubleVar(value=PERSON1_GAELD),

            "indtaegt_2"        : ctk.DoubleVar(value=PERSON2_LOEN), 
            "pension_2"         : ctk.DoubleVar(value=PERSON2_PENSION), 
            "opsparring_2"      : ctk.DoubleVar(value=PERSON2_SAVINGS),
            "gaeld_2"           : ctk.DoubleVar(value=PERSON2_GAELD),

            "samlet_indtaegt"   : ctk.DoubleVar(value=SAMLET_INDTAEGT),
            "max_laan"          : ctk.DoubleVar(value=MAX_LAAN),
            "lon_efter_skat1"   : ctk.DoubleVar(value=LOEN_EFTER_SKAT1),
            "lon_efter_skat2"   : ctk.DoubleVar(value=LOEN_EFTER_SKAT2),
            "skatteprocent1"    : ctk.DoubleVar(value=SKATTEPROCENT1),
            "skatteprocent2"    : ctk.DoubleVar(value=SKATTEPROCENT2),
            "samlet_efter_skat" : ctk.DoubleVar(value=SAMLET_INDTAEGT)
            }
        
    def init_udgift_parameters(self): 
        self.udgift_vars = {    
            "bolig_udgift"            : ctk.DoubleVar(value=EJER_UDGIFT), 
            "forbrug"                 : ctk.DoubleVar(value=FORBRUG), 
            "mad_dagligvare"          : ctk.DoubleVar(value=MAD_DAGLIGVARE),
            "transport"               : ctk.DoubleVar(value=TRANSPORT),
            "forsikringer"            : ctk.DoubleVar(value=FORSIKRINGER),
            "telefon_int_medie"       : ctk.DoubleVar(value=TELEFON_INT_MEDIE),
            "personlig_pleje_toej"    : ctk.DoubleVar(value=PERSONLIG_PLEJE_TOEJ),
            "fritid_fornoejelser"     : ctk.DoubleVar(value=FRITID_FORNOEJELSER),
            "pasning_fritidsaktiv"    : ctk.DoubleVar(value=PASNING_FRITIDSAKTIVITETER), 

            "flex_udgift_string1"     : ctk.StringVar(value=FLEXUDGSTRING1),
            "flex_udgift_var1"        : ctk.DoubleVar(value=FLEXUDGVAR1),
            "flex_udgift_string2"     : ctk.StringVar(value=FLEXUDGSTRING2),
            "flex_udgift_var2"        : ctk.DoubleVar(value=FLEXUDGVAR2),
            "flex_udgift_string3"     : ctk.StringVar(value=FLEXUDGSTRING3),
            "flex_udgift_var3"        : ctk.DoubleVar(value=FLEXUDGVAR3), 
            
            "gaeldsfaktor"            : ctk.DoubleVar(value=GÆLDSFAKTOR),
            "banklaan"                : ctk.DoubleVar(value=BANKLÅN),
            "realkreditlaan"          : ctk.DoubleVar(value=REALKREDITLÅN),
            "samlet_laan"             : ctk.DoubleVar(value=SAMLETLÅN),
            "alle_faste_udgifter"     : ctk.DoubleVar(value=ALLEFASTEUDGIFTER),
            "forventet_pris"          : ctk.DoubleVar(value=FORVENTETPRIS)
        }
        
    def init_fremtid_parameters(self): 
        self.fremtid_vars = {  
            "bolig_udgift"                  : ctk.DoubleVar(value=EJER_UDGIFT), 
            "realkredit_laaneperiode"       : ctk.IntVar(value=REAL_LÅNPERIODE), 
            "realkredit_nominel"            : ctk.DoubleVar(value=REAL_NOMINEL),
            "realkredit_bidragssats"        : ctk.DoubleVar(value=REAL_BIDRAGSSATS),
            "realkredit_terminer"           : ctk.IntVar(value=REAL_TERMINER),
            "afdragsfri"                    : ctk.BooleanVar(value=AFDRAGSFRI),

            "bank_nominel"                  : ctk.DoubleVar(value=BANK_NOMINEL),
            "bank_terminer"                 : ctk.IntVar(value=BANK_TERMINER),
            "bank_laaneperiode"             : ctk.IntVar(value=REAL_LÅNPERIODE),

            "rente_betaling"                : ctk.DoubleVar(value=RENTE_BETALING), 
            "rente_afdrag"                  : ctk.DoubleVar(value=RENTE_AFDRAG),  
            "rentefradrag"                  : ctk.DoubleVar(value=RENTEFRADRAG), 
            "rentefradrag_procent"          : ctk.DoubleVar(value=RENTEFRADRAGPROCENT), 
            "samlet_ydelse"                 : ctk.DoubleVar(value=SAMLET_YDELSE), 
            "fast_udgifter"                 : ctk.DoubleVar(value=FASTE_UDGIFTER), 
            "fast_udgifter_inkl_ydelser"    : ctk.DoubleVar(value=FASTE_UDGIFTER_INKL_YDELSER), 
            "raadighedsbeloeb"              : ctk.DoubleVar(value=RÅDIGHEDSBELØB)           
        }

        self.fremtid_dicts = {
            "realkredit_laaneberegning": BANK_LAANEBEREGNING,
            "bank_laaneberegning"      : REAL_LAANEBEREGNING,
        }

    def init_person_info_parameters (self): 
        self.person_info_vars = {  
            "Fornavn1"                          : ctk.StringVar (value=FORNAVN1), 
            "Efternavn1"                        : ctk.StringVar (value=EFTERNAVN1),             
            "telefon1"                          : ctk.StringVar (value=TELEFON1),
            "mail1"                             : ctk.StringVar (value=MAIL1),
            "adresse_vej1"                      : ctk.StringVar (value=ADRESSES_VEJ1),
            "adresse_postnr1"                   : ctk.StringVar (value=ADRESSE_POSTNR1),
            "adresse_by1"                       : ctk.StringVar (value=ADRESSE_BY1),
            "adresse_samlet1"                   : ctk.StringVar (value=ADRESSE_SAMLET2),
            "fodselsdag_dag1"                   : ctk.IntVar    (value=FØDSELSDAG_DAG1), 
            "fodselsdag_maaned1"                : ctk.IntVar    (value=FØDSELSDAG_MÅNED1), 
            "fodselsdag_aar1"                   : ctk.IntVar    (value=FØDSELSDAG_ÅR1), 
            "dato_dmo1"                         : ctk.StringVar (value=DATO_DMO1),

            "Fornavn2"                          : ctk.StringVar (value=FORNAVN2), 
            "Efternavn2"                        : ctk.StringVar (value=EFTERNAVN2), 
            "telefon2"                          : ctk.StringVar (value=TELEFON2),
            "mail2"                             : ctk.StringVar (value=MAIL2),            
            "adresse_vej2"                      : ctk.StringVar (value=ADRESSES_VEJ2),
            "adresse_postnr2"                   : ctk.StringVar (value=ADRESSE_POSTNR2),
            "adresse_by2"                       : ctk.StringVar (value=ADRESSE_BY2),
            "adresse_samlet2"                   : ctk.StringVar (value=ADRESSE_SAMLET2),
            "fodselsdag_dag2"                   : ctk.IntVar    (value=FØDSELSDAG_DAG2), 
            "fodselsdag_maaned2"                : ctk.IntVar    (value=FØDSELSDAG_MÅNED2), 
            "fodselsdag_aar2"                   : ctk.IntVar    (value=FØDSELSDAG_ÅR2), 
            "dato_dmo2"                         : ctk.StringVar (value=DATO_DMO2),

            "ny_adresse_vej"                    : ctk.StringVar (value=NY_ADDR),
            "link_til_ny_adresse"               : ctk.StringVar (value=LINK_ADDR),
            "rapportnavn"                       : ctk.StringVar (value=RAPPORTNAVN)
            }

    def init_Forhandling_parameters(self):
        self.forhandlings_vars = { 
            "udbudspris"        : ctk.StringVar(value=UDBUDSPRIS), 
            "forventet_procent" : ctk.StringVar(value=FORVENTET_PROCENT), 
            "forventet_pris"    : ctk.StringVar(value=FORVENTET_PRIS), 
            "runde1_procent"    : ctk.StringVar(value=RUNDE1_PROCENT), 
            "runde1_pris"       : ctk.StringVar(value=RUNDE1_PRIS), 
            "runde2_procent"    : ctk.StringVar(value=RUNDE2_PROCENT), 
            "runde2_pris"       : ctk.StringVar(value=RUNDE2_PRIS), 
            "runde3_procent"    : ctk.StringVar(value=RUNDE3_PROCENT), 
            "runde3_pris"       : ctk.StringVar(value=RUNDE3_PRIS), 
            "runde4_procent"    : ctk.StringVar(value=RUNDE4_PROCENT), 
            "runde4_pris"       : ctk.StringVar(value=RUNDE4_PRIS), 
            "aggressivitet"     : ctk.IntVar(value=AGGRESSIVITET),
            "forhandling_titel" : ctk.StringVar(value=FORHANDLING_TITEL),
            "strategi_titel"    : ctk.StringVar(value=FORHANDLING_STRATEGI),
            "losore_titel"      : ctk.StringVar(value=FORHANDLING_LØSØRE),
            "argument_titel"    : ctk.StringVar(value=FORHANDLING_ARGUMENT),
            } 


    def init_budgetvaerktoej_parameters(self):
         self.budgetvaerktoej_vars = { 
            'budget_titel'          : ctk.StringVar (value=BUDGETNAVN),
            'kontakt_navn'          : ctk.StringVar (value=KONTAKT_NAVN),
            'kontakt_telefon'       : ctk.StringVar (value=KONTAKT_TELEFON),
            'kontakt_mail'          : ctk.StringVar (value=KONTAKT_MAIL)
            }
                  

    def init_UGC_parameters(self):
        self.feedback_dict = {} 
        self.forhandlings_løsøre_dict = {}
        self.forhandlings_løsøre_inspiration_dict = LØSØRE_INSPIRATION

        self.forhandlings_argumenter_dict = {}
        self.forhandlings_argumenter_inspiration_dict = ARGUMENTER_INSPIRATION
        
        self.budgetvaerktoej_dict = {} 

        # gets all result functions for saves and db syncs. 
        self.all_UGC_update_functions = {}  

    def run_all_update_functions(self): 
        for updateFunc in self.all_UGC_update_functions.values():
            try: 
                updateFunc()
                print ("update func run")
                updateFunc()
            except: 
                print ("update func passed")
                pass
        

    def manipulate_forhandling(self, *args):
        # Udregn når variabler ændres
        fuMath.Ackerman_Set_Values(self.forhandlings_vars)

    # De fire hovedmenuer 
    def menu_finansierng(self): 
        self.hubview.grid_forget() # Hide import buttons
        self.current_view = Finansering(self, self.finansiering_vars, self.udgift_vars, self.fremtid_vars, self.person_info_vars,  mainApp=self)
        self.close_button = CloseSection(self, self.back_to_hub)
        self.feedback_button = Open_Feedback_button(self)

    def menu_forhandling(self): 
        self.hubview.grid_forget()
        self.current_view = Forhandling(self, self.forhandlings_vars)
        self.close_button = CloseSection(self, self.back_to_hub)
        self.feedback_button = Open_Feedback_button(self)
        
    def menu_budgetvaerktoej(self):
        self.hubview.grid_forget()
        self.current_view = Renovering(self, self.budgetvaerktoej_vars)
        self.close_button = CloseSection(self, self.back_to_hub)
        self.feedback_button = Open_Feedback_button(self)

    def back_to_hub(self):
        self.current_view.grid_forget()
        hub = self.to_hubview()
        self.current_view = hub

        # make sure all dicts are up to date. 
        self.run_all_update_functions()
        self.eksporter_data_til_db()
        

    def back_to_login_screen(self):
        # 1. Luk aktiv databaseforbindelse, hvis der er en
        # de bliver lukket hvergang jeg gemmer og henter nu 

        # 2. Nulstil brugerrelaterede data
        self.logged_in_email = None
        self.factory_parameter_settings() 
        self.logged_in = False

        # 3. Fjern nuværende visning og vis login
        # print ("CURRENT VIEW: ")
        # print("WIDGET MANAGER:", self.current_view.winfo_manager())
        # print(self.current_view.winfo_manager())  # viser om det er "grid", "pack" eller ""
        # print (self.current_view)

        try: 
            self.current_view.grid_forget()
        except: 
            pass
        
        self.show_login_view()

    def on_close(self):
        try:
            if self.logged_in: 
                self.eksporter_data_til_db()

        except Exception as e:
            print("Fejl ved luk:", e)

        self.destroy()

    def eksporter_data_til_db(self):
        # Export Vars
        vars_dicts = {
            "brugere": self.person_info_vars,
            "finansiering": self.finansiering_vars,
            "udgift": self.udgift_vars,
            "fremtid": self.fremtid_vars, 
            "budgetvaerktoej": self.budgetvaerktoej_vars,
            "forhandling": self.forhandlings_vars,
        }

        dbhandler.eksporter_vars_til_db(self.logged_in_email, vars_dicts)

        # export UGC
        ugc_dict = { 
        "argumentation": self.forhandlings_argumenter_dict,
        "loesoere": self.forhandlings_løsøre_dict,
        "feedback": self.feedback_dict,
        "budgetvaerktoej": self.budgetvaerktoej_dict,
        }

        dbhandler.eksporter_ugc_til_db(self.logged_in_email, ugc_dict)


    def importer_data_fra_db(self):
        # hent vars på db
        vars_dicts = {
            "brugere": self.person_info_vars,
            "finansiering": self.finansiering_vars,
            "udgift": self.udgift_vars,
            "fremtid": self.fremtid_vars,
            "budgetvaerktoej": self.budgetvaerktoej_vars,
            "forhandling": self.forhandlings_vars,
        }

        dbhandler.importer_vars_fra_db(self.logged_in_email, vars_dicts)

        # hent User generaated dictionaries
        ugc_dict = { 
        "feedback": self.feedback_dict,
        "argumentation": self.forhandlings_argumenter_dict,
        "loesoere": self.forhandlings_løsøre_dict,
        "budgetvaerktoej": self.budgetvaerktoej_dict,
        }
        dbhandler.importer_ugc_fra_db(self.logged_in_email, ugc_dict)
        #print ("UGC picked from DB")
        #print ("self.budgetvaerktoej_dict")

    # count down 
    def countdown(self):
                
        # return menu after 5 sec. 
        #self.seconds_left = 5 
        #self.countdown()
        print ('counter started')
        if self.seconds_left > 0:
            print (self.seconds_left)
            self.seconds_left -= 1
            self.after(1000, self.countdown)  
        else:
            print("Countdown done — Back to hubview!")
            self.to_hubview()


App() 
# Run app 
