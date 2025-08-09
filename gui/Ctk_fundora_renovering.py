
import customtkinter as ctk

from components.Ctk_fundora_panels import SingleInputPanel, ForhandlingsPanel, SliderPanel, DoubleInputPanel, ForhandlingCheckPanel, RenoveringsOpgavePanel, SimpleContactLinePanel, Bugetvaerktoej_handler
import backend.Ctk_fundora_math_lib as fuMath
import backend.Ctk_fundora_exportPDF as export 

from Ctk_fundora_loanerValues import *

class Renovering(ctk.CTkTabview): 
    def __init__(self, parent, rennovering_vars): 
        super().__init__(master = parent, fg_color=WHITE,
                         segmented_button_selected_color=PURPLE, 
                         segmented_button_selected_hover_color=LIGHT_PURPLE, 
                         segmented_button_unselected_hover_color=LIGHT_PURPLE, text_color=WHITE, border_color= ORANGE)
        self.grid(row=0, column=0, sticky='nsew', pady=10, padx=10)

        self.add("Budget")
        #self.add("Gantt Plan")
        #self.add("Huskeliste")
        #self.add("Eksport")

        Renovering_budget_tab(self.tab("Budget"), parent, rennovering_vars)
        #Renovering_huskeliste_tab(self.tab("Gantt Plan"), rennovering_vars)
        #Renovering_huskeliste_tab(self.tab("Huskeliste"), rennovering_vars)
        #Renovering_eksport_tab(self.tab("Eksport"), rennovering_vars)

class Renovering_budget_tab(ctk.CTkFrame): 
    def __init__(self, parent, mainApp, rennovering_vars): 
        super().__init__(master=parent, fg_color=WHITE)
        self.pack(expand=True, fill='both')
        self.columnconfigure(0, weight=1)
        
        # reference to maip
        self.mainApp = mainApp

        self.current_row_index = 1  # Track row numbers

        # budget navn
        self.budgetTitel_entry = ctk.CTkEntry(self, textvariable=rennovering_vars['budget_titel'], font=("Helvetica", 18, "bold"), justify="center")
        self.budgetTitel_entry.grid(row=0, column=0, sticky="new", padx=5, pady=5)

        # kontakt linje 
        #self.Kontakt_info = SimpleContactLinePanel(self, rennovering_vars) 
        self.kontaktFrame = ctk.CTkFrame(self, fg_color=WHITE)
        self.kontaktFrame.grid(row=1, column=0, sticky='new', padx=5, pady=(5,1))
        self.kontaktFrame.columnconfigure((0,1,2), weight=1)

        self.kontakt_navn_entry = ctk.CTkEntry   (self.kontaktFrame, placeholder_text = 'Kontaktperson', textvariable=rennovering_vars['kontakt_navn'],  justify="center")
        self.kontakt_telefon_entry = ctk.CTkEntry(self.kontaktFrame, placeholder_text = 'Telefon', textvariable=rennovering_vars['kontakt_telefon'],  justify="center")
        self.kontakt_mail_entry = ctk.CTkEntry   (self.kontaktFrame, placeholder_text = 'Email', textvariable=rennovering_vars['kontakt_mail'],  justify="center")

        self.kontakt_navn_entry.grid(row=0, column=0, sticky="new", padx=5, pady=5)
        self.kontakt_telefon_entry.grid(row=0, column=1, sticky="new", padx=5, pady=5)
        self.kontakt_mail_entry.grid(row=0, column=2, sticky="new", padx=5, pady=5)

        # Scrollable frame til opgaver
        self.OpgaveFrame = ctk.CTkScrollableFrame(self, fg_color=WHITE)
        self.OpgaveFrame.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)
        self.OpgaveFrame.columnconfigure((0,1,2,3), weight=1)
        self.OpgaveFrame.configure(height=550)  # eller den højde du synes passer

        # initier og tilføj budgetvaerktøj
        self.bugetvaerktoej_handler = Bugetvaerktoej_handler(self.mainApp, self.OpgaveFrame) 
        mainApp.all_UGC_update_functions["budgetvaerktoej_update_dict"] = self.bugetvaerktoej_handler.update_ref_dict


        # Frame for total result 
        # Udenfor opgave frame
        self.renovation_bottom_Frame = ctk.CTkFrame(self, fg_color=WHITE)
        self.renovation_bottom_Frame.grid(row=3, column=0, sticky="ew", padx=5, pady=5)
        self.renovation_bottom_Frame.columnconfigure((0,1,2,3,4,5,6,7,8,9,10), weight=1)  # ← allow frame to expand in its parent

        self.tilføj_renovation_button = ctk.CTkButton(self.renovation_bottom_Frame, 
                                                        text="+ tilføj Hovedoppgave", 
                                                        command=self.bugetvaerktoej_handler.tilføj_renovering,
                                                        corner_radius=32, 
                                                        hover_color=LIGHT_PURPLE, 
                                                        fg_color=PURPLE, 
                                                        border_color=PURPLE, 
                                                        text_color=WHITE_TEXT_COLOR,
                                                        font=("Helvetica", 14, "bold"),
                                                        border_width=2)
        self.tilføj_renovation_button.grid(row=0, column=0, columnspan=6,padx=5, pady=5,sticky="ew")
        
        # Eksporter         
        self.eksport_budget_button = ctk.CTkButton(self.renovation_bottom_Frame, 
                                                        text="Eksporter Budget PDF", 
                                                        command=self.bugetvaerktoej_handler.get_all_results, # command=lambda: export.Eksport_rennovation_budget_PDF(self.get_all_results(), rennovering_vars))
                                                        corner_radius=32, 
                                                        fg_color=DARK_ORANGE, 
                                                        hover_color=HIGHTLIGHT_ORANGE, 
                                                        border_color=DARK_ORANGE, 
                                                        text_color=WHITE_TEXT_COLOR,
                                                        font=("Helvetica", 14, "bold"),
                                                        border_width=2)

        self.eksport_budget_button.grid(row=0, column=6, columnspan=3,padx=5, pady=5,sticky="ew")

        # total pris knap         
        self.Udregn_total_pris = ctk.CTkButton(self.renovation_bottom_Frame, 
                                                        text="Udregn Total pris", 
                                                        command=self.Total_pris,
                                                        corner_radius=32,
                                                        fg_color=DARK_GREEN, 
                                                        hover_color=LIGHT_GREEN, 
                                                        border_color=DARK_GREEN, 
                                                        text_color=WHITE_TEXT_COLOR,
                                                        border_width=2, 
                                                        font=("Helvetica", 18, "bold"))
        
        self.Udregn_total_pris.grid(row=0, column=9, sticky="ew", padx=5, pady=5)

        self.total_pris_var = ctk.StringVar(value=" ") 
        self.total_pris = ctk.CTkEntry(self.renovation_bottom_Frame, textvariable=self.total_pris_var, font=("Helvetica", 18, "bold"))
        self.total_pris.grid(row=0, column=10, sticky="sew", padx=5, pady=5)
            
    def Total_pris(self): 
        # Gemmer alle resultater på db og henter dem igen, så de matcher.     
        alle_panel_data = self.bugetvaerktoej_handler.get_all_results()

        # Udregn min total pris
        total_pris = fuMath.beregn_total_budget_pris(alle_panel_data)
        print (total_pris)
        self.total_pris_var.set(total_pris)


class Renovering_plan_tab(ctk.CTkFrame): 
    def __init__(self, parent, rennovering_vars, renovering_hovedopgave_data, renovering_underopgave_data): 
        super().__init__(master=parent, fg_color=WHITE)
        self.pack(expand=True, fill='both')


class Renovering_huskeliste_tab(ctk.CTkFrame): 
    def __init__(self, parent, rennovering_vars): 
        super().__init__(master=parent, fg_color=WHITE)
        self.pack(expand=True, fill='both')

        FrameColoum1 = ctk.CTkFrame(self, fg_color=WHITE)
        FrameColoum1.grid(row=0, sticky='new', columnspan=3 ,column=0, padx=5, pady=5)

class Renovering_eksport_tab(ctk.CTkFrame): 
    def __init__(self, parent, rennovering_vars): 
        super().__init__(master=parent, fg_color=WHITE)
        self.pack(expand=True, fill='both')

        self.columnconfigure((0, 1), weight=1)

        # layout
        person_frame1 = ctk.CTkFrame(self, fg_color=WHITE)
        person_frame1.grid(row=1, column=0, columnspan=1, padx=5, pady=5, sticky='new')
        person_frame2 = ctk.CTkFrame(self, fg_color=WHITE)
        person_frame2.grid(row=1, column=1, columnspan=1, padx=5, pady=5, sticky='new')

                # Beregning 
        self.beregn_button = ctk.CTkButton(self, 
                                            text="Eksporter PDF", 
                                            corner_radius=32, 
                                            hover_color="#EC6E07", 
                                            fg_color='transparent', 
                                            border_color="#FF9100", 
                                            border_width=2, )
                    
        self.beregn_button.grid(row = 3, column=0, columnspan=2)

