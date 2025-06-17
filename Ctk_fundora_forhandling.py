import customtkinter as ctk
from Ctk_fundora_panels import SingleInputPanel, ForhandlingsPanel, SliderPanel, DoubleInputPanel, ForhandlingCheckPanel

class Forhandling(ctk.CTkTabview): 
    def __init__(self, parent, forhandlings_vars, forhandlings_Interesseliste_data, forhandlings_argumenter_data): 
        super().__init__(master = parent)
        self.grid(row=0, column=0, sticky='nsew', pady=10, padx=10)

        self.add("Konsessiv Forhandling")
        self.add("Strategi")
        self.add("Interesser")

        Ackerman_tab(self.tab("Konsessiv Forhandling"), forhandlings_vars)
        Strategi_tab(self.tab("Strategi"), forhandlings_argumenter_data)
        Interesser_tab(self.tab("Interesser"), forhandlings_Interesseliste_data)
        
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
   
class Strategi_tab(ctk.CTkFrame): 
    def __init__(self, parent, forhandlings_Argumenter_data): 
        super().__init__(master=parent, fg_color="transparent")
        self.pack(expand=True, fill='both')

        self.columnconfigure(0, weight=1)
        #self.rowconfigure(0, weight=1)

        FrameColoum1 = ctk.CTkFrame(self)
        FrameColoum1.grid(row=0, sticky='new', column=0, padx=5, pady=5)

        self.forhandlings_Argumenter_data = forhandlings_Argumenter_data

        # argumenter
        self.priority_options = {"Fordel": {"color": "#236752", "desc": "Skal prioriteres"},
                                 "Ulempe": {"color": "#1554c0", "desc": "Godt at få med"}}
        self.panel = ForhandlingCheckPanel(parent=FrameColoum1, checklist_data=self.forhandlings_Argumenter_data, priority_options=self.priority_options) # Get_results
        self.panel.pack(fill="both", expand=True)

        print_button = ctk.CTkButton(self, text="Print resultater", command=self.print_results)
        print_button.grid(row=1, column=0, pady=10, padx=10, sticky="new")

    def print_results(self):
        resultater = self.panel.get_results()
        for punkt, info in resultater.items():
            print(f"{punkt}: {info}")

    def get_checklist_results(self):
        return self.panel.get_results()


class Interesser_tab(ctk.CTkFrame): 
    def __init__(self, parent, forhandlings_Interesseliste_data): 
        super().__init__(master=parent, fg_color="transparent")
        self.pack(expand=True, fill='both')

        self.columnconfigure(0, weight=1)
        #self.rowconfigure(0, weight=1)

        FrameColoum1 = ctk.CTkFrame(self)
        FrameColoum1.grid(row=0, sticky='new', column=0, padx=5, pady=5)

        self.forhandlings_Interesseliste_data = forhandlings_Interesseliste_data

        # interesse 
        self.priority_options1 = {   "Vigtigt": {"color": "#236752", "desc": "Skal prioriteres"},
                                    "Bonus": {"color": "#1554c0", "desc": "Godt at få med"},
                                    "Ikke relevant": {"color": "#b71c62", "desc": "Springes over"}}
        self.panel = ForhandlingCheckPanel(parent=FrameColoum1, checklist_data=self.forhandlings_Interesseliste_data, priority_options=self.priority_options1) # Get_results
        self.panel.pack(fill="both", expand=True)

        print_button = ctk.CTkButton(self, text="Print resultater", command=self.print_results)
        print_button.grid(row=1, column=0, pady=10, padx=10, sticky="new")

    def print_results(self):
        resultater = self.panel.get_results()
        for punkt, info in resultater.items():
            print(f"{punkt}: {info}")


    def get_checklist_results(self):
        return self.panel.get_results()
