import customtkinter as ctk
from Ctk_fundora_panels import SingleInputPanel, ForhandlingsPanel, SliderPanel, DoubleInputPanel, ForhandlingCheckPanel, RenoveringsOpgavePanel
import Ctk_fundora_math_lib as fuMath

class Renovering(ctk.CTkTabview): 
    def __init__(self, parent, rennovering_vars, renovering_hovedopgave_data, renovering_underopgave_data): 
        super().__init__(master = parent)
        self.grid(row=0, column=0, sticky='nsew', pady=10, padx=10)

        self.add("Renoveringer")
        self.add("Plan")
        self.add("Huskeliste")
        self.add("Eksport")

        Renovering_renovation_tab(self.tab("Renoveringer"), rennovering_vars)
        Renovering_plan_tab(self.tab("Plan"), rennovering_vars, renovering_hovedopgave_data, renovering_underopgave_data)
        Renovering_huskeliste_tab(self.tab("Huskeliste"), rennovering_vars)
        Renovering_eksport_tab(self.tab("Eksport"), rennovering_vars)


class Renovering_renovation_tab(ctk.CTkFrame): 
    def __init__(self, parent, rennovering_vars): 
        super().__init__(master=parent, fg_color="transparent")
        self.pack(expand=True, fill='both')
        # self.columnconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.current_row_index = 1  # Track row numbers

        # ← HUSK du får grid/pack conflict hvis du smider button i samme "self" fordi panels er packed inherited fra panel class. 

        # Scrollable frame til opgaver
        self.OpgaveFrame = ctk.CTkScrollableFrame(self, label_text="Renoveringsopgaver")
        self.OpgaveFrame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.OpgaveFrame.columnconfigure((0,1,2,3), weight=1)
        self.OpgaveFrame.configure(height=500)  # eller den højde du synes passer

        # Udenfor opgave frame
        self.tilføj_renovation_button = ctk.CTkButton(self, 
                                                        text="+ tilføj Renovering", 
                                                        command=self.tilføj_renovering,
                                                        corner_radius=32, 
                                                        hover_color="#0798EC", 
                                                        fg_color='transparent', 
                                                        border_color="#0077FF", 
                                                        border_width=2)
        self.tilføj_renovation_button.grid(row=1, column=0, columnspan=3, pady=(0, 10), sticky="n")
        

        # Frame for total result 
        self.total_pris_Frame = ctk.CTkFrame(self)
        self.total_pris_Frame.grid(row=2, column=0, sticky="ew", padx=5, pady=5)
        self.total_pris_Frame.columnconfigure((0,1,2,3,4,5,6,7,8,9,10), weight=1)  # ← allow frame to expand in its parent
        
        self.tilføj_renovation_button = ctk.CTkButton(self.total_pris_Frame, 
                                                        text="Udregn Total pris", 
                                                        command=self.Total_pris, 
                                                        corner_radius=32,
                                                        hover_color="#EC6E07", 
                                                        fg_color='transparent',  
                                                        border_color="#FF9100", 
                                                        border_width=2)
        self.tilføj_renovation_button.grid(row=0, column=9, sticky="e", padx=5, pady=5)

        self.total_pris_var = ctk.StringVar(value=" ") 
        self.total_pris = ctk.CTkEntry(self.total_pris_Frame, textvariable=self.total_pris_var)
        self.total_pris.grid(row=0, column=10, sticky="sew", padx=5, pady=5)

            
        # Alle opgave paneler gemt. 
        self.opgave_panels = []  # Liste til alle opgave-paneler
        self.all_results = {}
        self.current_renovation_id = 1

    def tilføj_renovering(self, label_text="", checked=False, priority=None, comment=""):
        new_panel = RenoveringsOpgavePanel(self.OpgaveFrame, UID=self.current_renovation_id)
        self.current_renovation_id += 1

        self.opgave_panels.append(new_panel)  # Gem den nye panel        
        self.get_all_results()

    def get_all_results(self):
        for panel in self.opgave_panels:
            panel_results = panel.get_results()
            panel_name = panel.hovedopgave_navn_var.get() #.strip().replace(" ", "_")  # Ryd navn op
            # Brug det unikke ID som dict navn, så brugere kan navngive to renovationer samtidig. 
            self.all_results[panel.uid] = panel_results 
        
        print (self.all_results)
        return self.all_results

    def Total_pris(self): 
        # make sure you have latest of all results. 
        self.get_all_results()

        # calculate the total price from the dict. 
        total_pris = fuMath.beregn_total_pris(self.all_results)
        print (total_pris)
        self.total_pris_var.set(total_pris)

    # Ikke i brug længere
    def print_all_results(self):
        for idx, panel in enumerate(self.opgave_panels):
            print(f"Panel {idx + 1}:")
            resultater = panel.get_results()
            for opgave, info in resultater.items():
                print(f"  {opgave}: {info}")









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

