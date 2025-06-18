import customtkinter as ctk
from Ctk_fundora_panels import SingleInputPanel, ForhandlingsPanel, SliderPanel, DoubleInputPanel, ForhandlingCheckPanel

class Forhandling(ctk.CTkTabview): 
    def __init__(self, parent, forhandlings_vars, forhandlings_løsøre_data, forhandlings_argumenter_data): 
        super().__init__(master = parent)
        self.grid(row=0, column=0, sticky='nsew', pady=10, padx=10)

        self.add("Konsessiv Forhandling")
        self.add("Argumentation")
        self.add("Løsøre")
        self.add("Eksport")

        Ackerman_tab(self.tab("Konsessiv Forhandling"), forhandlings_vars)
        Argument_tab(self.tab("Argumentation"), forhandlings_argumenter_data, forhandlings_vars)
        Løsøre_tab(self.tab("Løsøre"), forhandlings_løsøre_data)
        Eksport_tab(self.tab("Eksport"), forhandlings_vars, forhandlings_løsøre_data, forhandlings_argumenter_data)
    
class Ackerman_tab(ctk.CTkFrame): 
    def __init__(self, parent, forhandlings_vars): 
        super().__init__(master=parent, fg_color="transparent")
        self.pack(expand=True, fill='both')
        self.columnconfigure((0,1,2), weight=1)

        FrameColoum1 = ctk.CTkFrame(self)
        FrameColoum1.grid(row=0, sticky='new', columnspan=3 ,column=0, padx=5, pady=5)
        SingleInputPanel(FrameColoum1, "Udbudspris", forhandlings_vars["udbudspris"])

        ForhandlingsPanel(FrameColoum1, "Forventet procent afslag & max købspris",  forhandlings_vars['forventet_procent'], forhandlings_vars['forventet_pris'], forhandlings_vars['udbudspris'])
        SliderPanel(FrameColoum1, "Koncessiv forhandlingsaggressivitet", "0", forhandlings_vars["aggressivitet"], 1, 3, defaultValue=1, step_size=1)
        
        outputFrame = ctk.CTkFrame(self)
        outputFrame.grid(row=1, sticky='new', columnspan=3 ,column=0, padx=5, pady=5)
        
        DoubleInputPanel(outputFrame, "1. Forhandlingsbud: ", forhandlings_vars['runde1_procent'], forhandlings_vars['runde1_pris'], readOption_A='disabled',  readOption_B='disabled') 
        DoubleInputPanel(outputFrame, "2. Forhandlingsbud: ", forhandlings_vars['runde2_procent'], forhandlings_vars['runde2_pris'], readOption_A='disabled',  readOption_B='disabled') 
        DoubleInputPanel(outputFrame, "3. Forhandlingsbud: ", forhandlings_vars['runde3_procent'], forhandlings_vars['runde3_pris'], readOption_A='disabled',  readOption_B='disabled') 
        DoubleInputPanel(outputFrame, "4. Forhandlingsbud: ", forhandlings_vars['runde4_procent'], forhandlings_vars['runde4_pris'], readOption_A='disabled',  readOption_B='disabled') 
   
class Argument_tab(ctk.CTkFrame): 
    def __init__(self, parent, forhandlings_Argumenter_data, forhandlings_vars): 
        super().__init__(master=parent, fg_color="transparent")
        self.pack(expand=True, fill='both')

        self.columnconfigure(0, weight=1)
        #self.rowconfigure(0, weight=1)

        FrameColoum1 = ctk.CTkFrame(self)
        FrameColoum1.grid(row=0, sticky='new', column=0, padx=5, pady=5)

        self.forhandlings_Argumenter_data = forhandlings_Argumenter_data

        # argumenter
        self.priority_options = {"Fordel": {"color": "#236752", "desc": "Skal prioriteres"},
                                 "Ulempe":  {"color": "#b71c62", "desc": "Springes over"}}
        
        # Refactor til var for bedre PDF eksport. example: forhandlings_var['Arg_label_Column0'] 
        self.columnLabels=['Til PDF', 'Argument', 'Fra købers perspektiv', 'Købers argumentation'] 

        self.panel = ForhandlingCheckPanel(parent=FrameColoum1, checklist_data=self.forhandlings_Argumenter_data, 
                                           priority_options=self.priority_options, AddCustomLine=False, columnLabels=self.columnLabels) # Get_results
        self.panel.pack(fill="both", expand=True)

        print_button = ctk.CTkButton(self, text="Print resultater", command=self.print_results)
        print_button.grid(row=1, column=0, pady=10, padx=10, sticky="new")

    def print_results(self):
        resultater = self.panel.get_results()
        for punkt, info in resultater.items():
            print(f"{punkt}: {info}")

    def get_checklist_results(self):
        return self.panel.get_results()


class Løsøre_tab(ctk.CTkFrame): 
    def __init__(self, parent, forhandlings_løsøre_data): 
        super().__init__(master=parent, fg_color="transparent")
        self.pack(expand=True, fill='both')

        self.columnconfigure(0, weight=1)
        #self.rowconfigure(0, weight=1)

        FrameColoum1 = ctk.CTkFrame(self)
        FrameColoum1.grid(row=0, sticky='new', column=0, padx=5, pady=5)

        self.forhandlings_løsøre_data = forhandlings_løsøre_data

        # interesse 
        self.priority_options1 = {   "Vigtigt": {"color": "#236752", "desc": "Skal prioriteres"},
                                    "Bonus": {"color": "#1554c0", "desc": "Godt at få med"},
                                    "Ikke relevant": {"color": "#b71c62", "desc": "Springes over"}}
        
        self.columnLabels=['Forhandlet', 'Løsøre', 'Vigtighed', 'Egne noter'] 

        self.panel = ForhandlingCheckPanel(parent=FrameColoum1, checklist_data=self.forhandlings_løsøre_data, 
                                           priority_options=self.priority_options1, columnLabels=self.columnLabels) 
        self.panel.pack(fill="both", expand=True)

        print_button = ctk.CTkButton(self, text="Print resultater", command=self.print_results)
        print_button.grid(row=1, column=0, pady=10, padx=10, sticky="new")

    def print_results(self):
        resultater = self.panel.get_results()
        for punkt, info in resultater.items():
            print(f"{punkt}: {info}")

    def get_checklist_results(self):
        return self.panel.get_results()


class Eksport_tab(ctk.CTkFrame): 
    def __init__(self, parent, forhandlings_vars, forhandlings_løsøre_data, forhandlings_argumenter_data): 
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
