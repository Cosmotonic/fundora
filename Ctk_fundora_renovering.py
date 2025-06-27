
import customtkinter as ctk

from Ctk_fundora_panels import SingleInputPanel, ForhandlingsPanel, SliderPanel, DoubleInputPanel, ForhandlingCheckPanel, RenoveringsOpgavePanel
import Ctk_fundora_math_lib as fuMath
import Ctk_fundora_exportPDF as export 


class Renovering(ctk.CTkTabview): 
    def __init__(self, parent, rennovering_vars, renovering_hovedopgave_data, renovering_underopgave_data): 
        super().__init__(master = parent)
        self.grid(row=0, column=0, sticky='nsew', pady=10, padx=10)

        self.add("Budget")
        #self.add("Plan")
        #self.add("Huskeliste")
        #self.add("Eksport")

        Renovering_budget_tab(self.tab("Budget"), rennovering_vars)
        #Renovering_plan_tab(self.tab("Plan"), rennovering_vars, renovering_hovedopgave_data, renovering_underopgave_data)
        #Renovering_huskeliste_tab(self.tab("Huskeliste"), rennovering_vars)
        #Renovering_eksport_tab(self.tab("Eksport"), rennovering_vars)


class Renovering_budget_tab(ctk.CTkFrame): 
    def __init__(self, parent, rennovering_vars): 
        super().__init__(master=parent, fg_color="transparent")
        self.pack(expand=True, fill='both')
        # self.columnconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.current_row_index = 1  # Track row numbers

        # ← HUSK du får grid/pack conflict hvis du smider button i samme "self" fordi panels er packed inherited fra panel class. 

        # Scrollable frame til opgaver
        self.BudgetTitel = ctk.StringVar(value="--- ANGIV BUDGET NAVN HER --- ")
        self.budgetTitel_entry = ctk.CTkEntry(self, textvariable=self.BudgetTitel, font=("Helvetica", 18, "bold"), justify="center")
        self.budgetTitel_entry.grid(row=0, column=0, sticky="new", padx=5, pady=5)
               
        self.OpgaveFrame = ctk.CTkScrollableFrame(self) #  label_text=self.BudgetTitel)
        self.OpgaveFrame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        self.OpgaveFrame.columnconfigure((0,1,2,3), weight=1)
        self.OpgaveFrame.configure(height=550)  # eller den højde du synes passer

        # Frame for total result 
        # Udenfor opgave frame
        self.renovation_bottom_Frame = ctk.CTkFrame(self)
        self.renovation_bottom_Frame.grid(row=2, column=0, sticky="ew", padx=5, pady=5)
        self.renovation_bottom_Frame.columnconfigure((0,1,2,3,4,5,6,7,8,9,10), weight=1)  # ← allow frame to expand in its parent

        self.tilføj_renovation_button = ctk.CTkButton(self.renovation_bottom_Frame, 
                                                        text="+ tilføj Renovering", 
                                                        command=self.tilføj_renovering,
                                                        corner_radius=32, 
                                                        hover_color="#0798EC", 
                                                        fg_color='transparent', 
                                                        border_color="#0077FF", 
                                                        border_width=2, 
                                                         font=("Helvetica", 18, "bold"))
        self.tilføj_renovation_button.grid(row=0, column=0, columnspan=6,padx=5, pady=5,sticky="ew")
        
        # Eksporter         
        self.eksport_budget_button = ctk.CTkButton(self.renovation_bottom_Frame, 
                                                        text="Eksporter Budget PDF", 
                                                        corner_radius=32, 
                                                        hover_color="#00CF79", 
                                                        fg_color='transparent', 
                                                        border_color="#00B871", 
                                                        border_width=2, 
                                                        font=("Helvetica", 18, "bold"),
                                                        command=lambda: export.Eksport_rennovation_budget_PDF(self.get_all_results(), budgetNavn=self.BudgetTitel.get()))

        self.eksport_budget_button.grid(row=0, column=6, columnspan=3,padx=5, pady=5,sticky="ew")

        # total pris knap         
        self.Udregn_total_pris = ctk.CTkButton(self.renovation_bottom_Frame, 
                                                        text="Udregn Total pris", 
                                                        command=self.Total_pris, 
                                                        corner_radius=32,
                                                        hover_color="#EC6E07", 
                                                        fg_color='transparent',  
                                                        border_color="#FF9100", 
                                                        border_width=2, 
                                                         font=("Helvetica", 18, "bold"))
        self.Udregn_total_pris.grid(row=0, column=9, sticky="ew", padx=5, pady=5)

        self.total_pris_var = ctk.StringVar(value=" ") 
        self.total_pris = ctk.CTkEntry(self.renovation_bottom_Frame, textvariable=self.total_pris_var, font=("Helvetica", 18, "bold"))
        self.total_pris.grid(row=0, column=10, sticky="sew", padx=5, pady=5)
            
        # Alle opgave paneler gemt. 
        self.opgave_panels = []  # Liste til alle opgave-paneler
        self.current_renovation_id = 1

    def tilføj_renovering(self, label_text="", checked=False, priority=None, comment=""):
        new_panel = RenoveringsOpgavePanel(self.OpgaveFrame, delete_callback=self.delete_renovation, UID=self.current_renovation_id)
        self.current_renovation_id += 1

        self.opgave_panels.append(new_panel)  # Gem den nye panel        

    def get_all_results(self):
        result = {}
        for panel in self.opgave_panels:
            panel_results = panel.get_results()
            result[panel.uid] = {
                "inkluder_i_budget": panel.inkluder_budget_var.get(),
                "hovedoppgave_navn": panel.Hovedoppgave_navn_var.get(), # <-- tilføj navnet
                "opgaver": panel_results,
            }
        return result

    def Total_pris(self): 
        # make sure you have latest of all results. 

        alle_panel_data = self.get_all_results()

        # Udregn min total pris
        total_pris = fuMath.beregn_total_pris(alle_panel_data)
        print (total_pris)
        self.total_pris_var.set(total_pris)

    # Ikke i brug længere
    def print_all_results(self):
        for idx, panel in enumerate(self.opgave_panels):
            print(f"Panel {idx + 1}:")
            resultater = panel.get_results()
            for opgave, info in resultater.items():
                print(f"  {opgave}: {info}")

    def delete_renovation(self, panel):
        panel.destroy()  # Fjern fra UI
        self.opgave_panels.remove(panel)  # fjern fra min liste


class Renovering_plan_tab(ctk.CTkFrame): 
    def __init__(self, parent, rennovering_vars, renovering_hovedopgave_data, renovering_underopgave_data): 
        super().__init__(master=parent, fg_color="transparent")
        self.pack(expand=True, fill='both')


class Renovering_huskeliste_tab(ctk.CTkFrame): 
    def __init__(self, parent, rennovering_vars): 
        super().__init__(master=parent, fg_color="transparent")
        self.pack(expand=True, fill='both')

        FrameColoum1 = ctk.CTkFrame(self)
        FrameColoum1.grid(row=0, sticky='new', columnspan=3 ,column=0, padx=5, pady=5)

class Renovering_eksport_tab(ctk.CTkFrame): 
    def __init__(self, parent, rennovering_vars): 
        super().__init__(master=parent, fg_color="transparent")
        self.pack(expand=True, fill='both')

        self.columnconfigure((0, 1), weight=1)

        # layout
        person_frame1 = ctk.CTkFrame(self)
        person_frame1.grid(row=1, column=0, columnspan=1, padx=5, pady=5, sticky='new')
        person_frame2 = ctk.CTkFrame(self)
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

