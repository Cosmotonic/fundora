# Lav ny Class hver gang den skal kaldes fra main scriptet. Image_output Image_Import

import customtkinter as ctk
import Ctk_fundora_exportPDF as export 
import ctk_fundora_math_lib as fuMath 

from Ctk_fundora_loanerValues import *
from Ctk_fundora_hubview import * 
from Ctk_fundora_forhandling import * 
from Ctk_fundora_finansiering import * 

class App(ctk.CTk): 
    def __init__(self):
        super().__init__()
        
        self.current_view = None

        # Setup 
        ctk.set_appearance_mode('dark') # ("light")
        self.geometry('1280x720')
        self.title('Fundora 1.0')
        self.minsize(800,500)
        
        self.init_Finansiering_parameters()
        self.init_Forhandling_parameters()
        self.init_udgift_parameters()
        self.init_fremtid_parameters()
        self.init_eksport_parameters()

        # Load hubview 
        self.to_hubview()

        # Let the main App window stretch
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # initiate window 
        self.mainloop()

    def to_hubview(self):
        self.hubview = hubview(self, finansiering = self.menu_Finansierng, forhandling = self.menu_forhandling, købet = self.menu_Koebet, rennovering = self.menu_Rennovering) 

        # Only trace needed values. Or use all:  combined_vars = list(self.forhandlings_vars.values()) 
        self.combined = [self.forhandlings_vars['aggressivitet'], self.forhandlings_vars['forventet_pris'], self.forhandlings_vars['forventet_procent']]
        for var in self.combined:
            var.trace('w', self.manipulate_forhandling)

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

            "Samlet_Indtægt"    : ctk.DoubleVar(value=SAMLET_INDTAEGT),
            "max_lån"           : ctk.DoubleVar(value=MAX_LAAN),
            "løn_efter_skat1"   : ctk.DoubleVar(value=LOEN_EFTER_SKAT1),
            "løn_efter_skat2"   : ctk.DoubleVar(value=LOEN_EFTER_SKAT2),
            "skatteprocent1"    : ctk.DoubleVar(value=SKATTEPROCENT1),
            "skatteprocent2"    : ctk.DoubleVar(value=SKATTEPROCENT2),
            "samlet_efter_skat" : ctk.DoubleVar(value=SAMLET_INDTAEGT)
            }
        
    def init_udgift_parameters(self): 
        self.udgift_vars = {    
            "bolig_udgift"              : ctk.DoubleVar(value=EJER_UDGIFT), 
            "forbrug"                   : ctk.DoubleVar(value=FORBRUG), 
            "mad_dagligvare"            : ctk.DoubleVar(value=MAD_DAGLIGVARE),
            "transport"                 : ctk.DoubleVar(value=TRANSPORT),
            "forsikringer"              : ctk.DoubleVar(value=FORSIKRINGER),
            "telefon_int_medie"         : ctk.DoubleVar(value=TELEFON_INT_MEDIE),
            "personlig_pleje_toej"      : ctk.DoubleVar(value=PERSONLIG_PLEJE_TOEJ),
            "fritid_fornoejelser"       : ctk.DoubleVar(value=FRITID_FORNOEJELSER),
            "pasning_fritidsaktiv"      : ctk.DoubleVar(value=PASNING_FRITIDSAKTIVITETER), 

            "flexUdgiftString1"         : ctk.StringVar(value=FLEXUDGSTRING1),
            "flexUdgiftVar1"            : ctk.DoubleVar(value=FLEXUDGVAR1),
            "flexUdgiftString2"         : ctk.StringVar(value=FLEXUDGSTRING2),
            "flexUdgiftVar2"            : ctk.DoubleVar(value=FLEXUDGVAR2),
            "flexUdgiftString3"         : ctk.StringVar(value=FLEXUDGSTRING3),
            "flexUdgiftVar3"            : ctk.DoubleVar(value=FLEXUDGVAR3), 
            
            "gældsfaktor"               : ctk.DoubleVar(value=GÆLDSFAKTOR),
            "banklån"                   : ctk.DoubleVar(value=BANKLÅN),
            "realkreditlån"             : ctk.DoubleVar(value=REALKREDITLÅN),
            "samlet_lån"                : ctk.DoubleVar(value=SAMLETLÅN),
            "alle_faste_udgifter"       : ctk.DoubleVar(value=ALLEFASTEUDGIFTER),
            "forventet_pris"            : ctk.DoubleVar(value=FORVENTETPRIS)
            }
        
    def init_fremtid_parameters(self): 
        self.fremtid_vars = {  
            "bolig_udgift"                  : ctk.DoubleVar (value=EJER_UDGIFT), 
            "realkredit_låneperiode"        : ctk.IntVar    (value=REAL_LÅNPERIODE ), 
            "realkredit_nominel"            : ctk.DoubleVar (value=REAL_NOMINEL),
            "realkredit_bidragssats"        : ctk.DoubleVar (value=REAL_BIDRAGSSATS),
            "realkredit_terminer"           : ctk.IntVar    (value=REAL_TERMINER),
            "afdragsfri"                    : ctk.BooleanVar(value=AFDRAGSFRI),
            "realkredit_låneberegning"      : BANK_LAANEBEREGNING, 

            "bank_nominel"                  : ctk.DoubleVar (value=BANK_NOMINEL),
            "bank_terminer"                 : ctk.IntVar    (value=BANK_TERMINER),
            "bank_låneperiode"              : ctk.IntVar    (value=REAL_LÅNPERIODE),
            "bank_låneberegning"            : BANK_LAANEBEREGNING, 

            "rente_betaling"                : ctk.DoubleVar(value=RENTE_BETALING), 
            "rente_afdrag"                  : ctk.DoubleVar(value=RENTE_AFDRAG),  
            "rentefradrag"                  : ctk.DoubleVar(value=RENTEFRADRAG), 
            "Rentefradrag_procent"          : ctk.DoubleVar(value=RENTEFRADRAGPROCENT), 
            "samlet_ydelse"                 : ctk.DoubleVar(value=SAMLET_YDELSE), 
            "fast_udgifter"                 : ctk.DoubleVar(value=FASTE_UDGIFTER), 
            "fast_udgifter_inkl_ydelser"    : ctk.DoubleVar(value=FASTE_UDGIFTER_INKL_YDELSER), 
            "rådighedsbeløb"                : ctk.DoubleVar(value=RÅDIGHEDSBELØB)           
            }

    def init_eksport_parameters(self): 
        self.eksport_vars = {  
            "Fornavn1"                          : ctk.StringVar (value=FORNAVN1), 
            "Efternavn1"                        : ctk.StringVar (value=EFTERNAVN1),             
            "telefon1"                          : ctk.StringVar (value=TELEFON1),
            "mail1"                             : ctk.StringVar (value=MAIL1),
            "Adresse_vej1"                      : ctk.StringVar (value=ADRESSES_VEJ1),
            "Adresse_postnr1"                   : ctk.StringVar (value=ADRESSE_POSTNR1),
            "Adresse_by1"                       : ctk.StringVar (value=ADRESSE_BY1),
            "SamletAdresse1"                    : ctk.StringVar (value=ADRESSE_SAMLET2),
            "fødselsdag_dag1"                   : ctk.IntVar    (value=FØDSELSDAG_DAG1), 
            "fødselsdag_måned1"                 : ctk.IntVar    (value=FØDSELSDAG_MÅNED1), 
            "fødselsdag_år1"                    : ctk.IntVar    (value=FØDSELSDAG_ÅR1), 
            "fødselsdag_DMÅ1"                   : ctk.StringVar (value=DATO_DMO1),

            "Fornavn2"                          : ctk.StringVar (value=FORNAVN2), 
            "Efternavn2"                        : ctk.StringVar (value=EFTERNAVN2), 
            "telefon2"                          : ctk.StringVar (value=TELEFON2),
            "mail2"                             : ctk.StringVar (value=MAIL2),            
            "Adresse_vej2"                      : ctk.StringVar (value=ADRESSES_VEJ2),
            "Adresse_postnr2"                   : ctk.StringVar (value=ADRESSE_POSTNR2),
            "Adresse_by2"                       : ctk.StringVar (value=ADRESSE_BY2),
            "SamletAdresse1"                    : ctk.StringVar (value=ADRESSE_SAMLET2),
            "fødselsdag_dag2"                   : ctk.IntVar    (value=FØDSELSDAG_DAG2), 
            "fødselsdag_måned2"                 : ctk.IntVar    (value=FØDSELSDAG_MÅNED2), 
            "fødselsdag_år2"                    : ctk.IntVar    (value=FØDSELSDAG_ÅR2), 
            "fødselsdag_DMÅ2"                   : ctk.StringVar (value=DATO_DMO2),

            "Ny_Adresse_Navn"                   : ctk.StringVar (value=NY_ADDR),
            "Link_adresse"                      : ctk.StringVar (value=LINK_ADDR),
            "Lånrapport"                        : ctk.StringVar (value=RAPPORTNAVN)
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
            "aggressivitet"     : ctk.IntVar(value=AGGRESSIVITET)
            } 
        
    def manipulate_forhandling(self, *args):
        # Udregn når variabler ændres
        fuMath.Ackerman_Set_Values(self.forhandlings_vars)

    # De fire hovedmenuer 
    def menu_Finansierng(self): 
        print ('Finansiering menu')
        self.hubview.grid_forget() # Hide import buttons
        self.current_view = Finansering(self, self.finansiering_vars, self.udgift_vars, self.fremtid_vars, self.eksport_vars)
        self.close_button = CloseSection(self, self.back_to_hub)
        
        # return menu after 5 sec. 
        #self.seconds_left = 5 
        #self.countdown()

    def menu_forhandling(self): 
        print ('Forhandling menu')
        self.hubview.grid_forget()
        self.current_view = Forhandling(self, self.forhandlings_vars)
        self.close_button = CloseSection(self, self.back_to_hub)
        
    def menu_Koebet(self): 
        print ('Koebet menu')
        self.hubview.grid_forget()
        # self.current_view = Koebet(self, self.forhandlings_vars)
        self.close_button = CloseSection(self, self.back_to_hub)

    def menu_Rennovering(self):
        print ('Rennovering menu')
        # self.current_view = Rennovering(self, self.forhandlings_vars)
        self.hubview.grid_forget()

    def back_to_hub(self):
        print ('Back to Hub view')
        self.current_view.grid_forget()
        self.to_hubview()

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
