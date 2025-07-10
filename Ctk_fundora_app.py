# Lav ny Class hver gang den skal kaldes fra main scriptet. Image_output Image_Import
# brug alle udnerfoldere 
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), ".")))

import customtkinter as ctk
import backend.Ctk_fundora_exportPDF as export 
import backend.Ctk_fundora_math_lib as fuMath 

from Ctk_fundora_loanerValues import *
from gui.Ctk_fundora_hubview import * 
from gui.Ctk_fundora_forhandling import * 
from gui.Ctk_fundora_finansiering import * 
from gui.Ctk_fundora_renovering import * 
from gui.Ctk_fundora_loginview import LoginFrame



class App(ctk.CTk): 
    def __init__(self):
        super().__init__()
        self.current_view = None
        ctk.set_appearance_mode('dark')
        self.geometry('1280x720')
        self.title('Fundora 0.2')
        self.minsize(800,500)

        # set all parameters. Needs def so it can be called after logout and login. 
        self.reset_all_parameters()

        # Start med login view
        self.show_login_view()

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.mainloop()

    def show_login_view(self):
        if self.current_view:
            self.current_view.destroy()
        self.current_view = LoginFrame(self, on_success=self.on_login_success)
        self.current_view.grid(row=0, column=0, sticky="nsew")

    def on_login_success(self, email):
        self.logged_in_email = email
        self.to_hubview()  # Når login er korrekt
        self.reset_all_parameters() # Reset to default config params. 
        # self.import_data_fra_db() # skal laves. 

    def to_hubview(self):
        self.hubview = hubview(self, self.importer_data_fra_db, self.eksporter_data_til_db, logout_callback=self.back_to_login, finansiering = self.menu_Finansierng, forhandling = self.menu_forhandling,rennovering = self.menu_Renovering)  # 

        # Only trace needed values. Or use all:  combined_vars = list(self.forhandlings_vars.values()) 
        self.combined = [self.forhandlings_vars['aggressivitet'], self.forhandlings_vars['forventet_pris'], self.forhandlings_vars['forventet_procent']]
        for var in self.combined:
            var.trace('w', self.manipulate_forhandling)

    def reset_all_parameters(self):
        self.init_Finansiering_parameters()
        self.init_Forhandling_parameters()
        self.init_udgift_parameters()
        self.init_fremtid_parameters()
        self.person_info_parameters()
        self.init_renovering_parameters()

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

            "samlet_indtaegt"    : ctk.DoubleVar(value=SAMLET_INDTAEGT),
            "max_laan"           : ctk.DoubleVar(value=MAX_LAAN),
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

    def person_info_parameters (self): 
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
            "Forhandling_Titel" : ctk.StringVar(value=FORHANDLING_TITEL),
            "strategi_titel"    : ctk.StringVar(value=FORHANDLING_STRATEGI),
            "løsære_titel"      : ctk.StringVar(value=FORHANDLING_LØSØRE),
            "argument_titel"    : ctk.StringVar(value=FORHANDLING_ARGUMENT),
            } 

                
        self.forhandlings_løsøre_data = {
            "Pris": {"checked": True, "priority": "Vigtigt", "comment": "Ønske om reduktion på 100.000 kr"},
            "Overtagelsesdato": {"checked": True, "priority": "Bonus", "comment": "Senest 1. august"},
            "Gardiner": {"checked": True, "priority": "Ikke relevant", "comment": "Medbringes selv ved indflytning"},
            "Skabe og opbevaring": {"checked": True, "priority": "Bonus", "comment": "Indbyggede skabe ønskes inkluderet"},
            "Forbedringer": {"checked": True, "priority": "Vigtigt", "comment": "Ønsker kompensation for manglende vedligehold"},
            "Hvidevarer": {"checked": True, "priority": "Bonus", "comment": "Alle hvidevarer ønskes inkluderet i handlen"},
            "Aconto og restancer": {"checked": True, "priority": "Vigtigt", "comment": "Ingen gamle regninger må overdrages"},
            "Vedligeholdelsesplan": {"checked": True, "priority": "Bonus", "comment": "Ønske om indsigt i kommende udgifter"},
            "Møbler": {"checked": True, "priority": "Bonus", "comment": "Spisebord og sofa må gerne blive"},
            "Havemøbler ": {"checked": True, "priority": "Bonus", "comment": "Terrassemøbler kan indgå i prisen"},
            "Haveredskaber": {"checked": True, "priority": "Bonus", "comment": "Redskaber ønskes efterladt i skuret"}
            }

        self.forhandlings_argumenter_data = {
            "Liggetid": {"checked": True, "priority": "Fordel", "comment": ""},
            "Boligmarkedet": {"checked": True, "priority": "Ulempe", "comment": "Det er sælgers markede"},
            "Prisniveau i området": {"checked": True, "priority": "Fordel", "comment": "Sammenlignelige boliger sælges billigere"},
            "Stand og vedligeholdelse": {"checked": True, "priority": "Ulempe", "comment": "Boligen kræver istandsættelse"},
            "Boligens størrelse og planløsning": {"checked": True, "priority": "Fordel", "comment": "Planløsningen er ikke optimal"},
            "Tidspres for sælger": {"checked": True, "priority": "Fordel", "comment": "Sælger virker ivrig for hurtig overtagelse"},
            "Ejendomsskat og fællesudgifter": {"checked": True, "priority": "Ulempe", "comment": "Høje faste udgifter påvirker købers økonomi"},
            "Udbud og efterspørgsel": {"checked": True, "priority": "Fordel", "comment": "Få interesserede og mange boliger i området"},
            "Naboer eller støjforhold": {"checked": True, "priority": "Ulempe", "comment": "Støj fra vej eller naboejendom"},
            "Tilstandsrapport eller energimærke": {"checked": True, "priority": "Fordel", "comment": "Dårlig energimærkning åbner for rabat"}
            }

    def init_renovering_parameters(self):
         self.renovering_vars = { 
            'budget_titel'           : ctk.StringVar (value=BUDGETNAVN),
            'kontakt_navn'          : ctk.StringVar (value=KONTAKT_NAVN),
            'kontakt_telefon'       : ctk.StringVar (value=KONTAKT_TELEFON),
            'kontakt_mail'          : ctk.StringVar (value=KONTAKT_MAIL)
            }
                  
         self.renovering_hovedopgave_data = {
            "Badeværelse": {"priority": "Skal"},
            }                  
         self.renovering_underopgave_data = {
            "VVS": {"prioritet": 1, "kommentar": "Køkkent skal laves først, så vi kan lave VVS på samme dag.", "tidsforbrug": 10, "løn/håndværker": 5000 },
            }

    def manipulate_forhandling(self, *args):
        # Udregn når variabler ændres
        fuMath.Ackerman_Set_Values(self.forhandlings_vars)

    # De fire hovedmenuer 
    def menu_Finansierng(self): 
        self.hubview.grid_forget() # Hide import buttons
        self.current_view = Finansering(self, self.finansiering_vars, self.udgift_vars, self.fremtid_vars, self.person_info_vars,  mainApp=self)
        self.close_button = CloseSection(self, self.back_to_hub)
        
        # return menu after 5 sec. 
        #self.seconds_left = 5 
        #self.countdown()

    def menu_forhandling(self): 
        self.hubview.grid_forget()
        self.current_view = Forhandling(self, self.forhandlings_vars, self.forhandlings_løsøre_data, self.forhandlings_argumenter_data)
        self.close_button = CloseSection(self, self.back_to_hub)
        
    def menu_Koebet(self): 
        self.hubview.grid_forget()
        self.close_button = CloseSection(self, self.back_to_hub)

    def menu_Renovering(self):
        self.hubview.grid_forget()
        self.current_view = Renovering(self, self.renovering_vars, self.renovering_hovedopgave_data, self.renovering_underopgave_data)
        self.close_button = CloseSection(self, self.back_to_hub)

    def back_to_hub(self):
        self.current_view.grid_forget()
        self.to_hubview()

    def back_to_login(self):
        self.current_view.grid_forget()
        self.show_login_view()        


    # eksporter alle variabler på person data 
    def eksporter_data_til_db(self):
        data = {}

        for var_dict in [self.finansiering_vars, self.udgift_vars, self.fremtid_vars, self.person_info_vars]:
        
            for key, var in var_dict.items():
                try:
                    data[key.lower()] = var.get()
                except Exception as e:
                    print(f"Fejl ved hentning af '{key}': {e}")

        from database.Fundora_data_handler import gem_person_data
        gem_person_data(self.logged_in_email, data)

    def importer_data_fra_db(self):
        from database.Fundora_data_handler import hent_person_data

        data = hent_person_data(self.logged_in_email)

        if not data:
            print("Ingen data fundet for bruger.")
            return

        # Liste over alle variable-dictionaries
        all_var_dicts = [
            self.person_info_vars,
            self.finansiering_vars,
            self.udgift_vars,
            self.fremtid_vars,
            self.renovering_vars,
        ]

        for var_dict in all_var_dicts:
            for key, var in var_dict.items():
                try:
                    value = data.get(key.lower())
                    if value is not None:
                        var.set(value)
                    else:
                        # Reset til default, hvis data mangler
                        var.set("" if isinstance(var, ctk.StringVar) else 0)
                except Exception as e:
                    print(f"Fejl ved indsætning af '{key}': {e}")




    # count down 
    def countdown(self):
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
