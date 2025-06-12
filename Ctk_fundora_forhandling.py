import customtkinter as ctk
from Ctk_fundora_panels import SingleInputPanel, ForhandlingsPanel, SliderPanel, DoubleInputPanel

class Forhandling(ctk.CTkTabview): 
    def __init__(self, parent, forhandlings_vars ): 
        super().__init__(master = parent)
        self.grid(row=0, column=0, sticky='nsew', pady=10, padx=10)

        self.add("Processen")
        self.add("Strategi")

        Ackerman_tab(self.tab("Processen"), forhandlings_vars)
        Strategi_tab(self.tab("Strategi"))
        
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
    def __init__(self, parent): 
        super().__init__(master=parent, fg_color="transparent")
        self.pack(expand=True, fill='both')

        self.columnconfigure((0,1,2), weight=1)
      
        FrameColoum1 = ctk.CTkFrame(self)
        FrameColoum1.grid(row=0, sticky='new',column=0, padx=5, pady=5)
        FrameColoum2 = ctk.CTkFrame(self)
        FrameColoum2.grid(row=0, sticky='new',column=1, padx=5, pady=5)
        FrameColoum3 = ctk.CTkFrame(self)
        FrameColoum3.grid(row=0, sticky='new',column=2, padx=5, pady=5)