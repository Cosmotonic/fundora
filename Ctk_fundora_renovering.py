import customtkinter as ctk
from Ctk_fundora_panels import SingleInputPanel, ForhandlingsPanel, SliderPanel, DoubleInputPanel, ForhandlingCheckPanel


class Renovering(ctk.CTkTabview): 
    def __init__(self, parent, rennovering_vars, renoveings_data): 
        super().__init__(master = parent)
        self.grid(row=0, column=0, sticky='nsew', pady=10, padx=10)

        self.add("Renoveringer")
        self.add("Plan")
        self.add("Huskeliste")
        self.add("Eksport")

        Renovering_renovation_tab(self.tab("Renoveringer"), rennovering_vars)
        Renovering_plan_tab(self.tab("Plan"), rennovering_vars)
        Renovering_huskeliste_tab(self.tab("Huskeliste"), rennovering_vars)
        Renovering_eksport_tab(self.tab("Eksport"), rennovering_vars)


class Renovering_renovation_tab(ctk.CTkFrame): 
    def __init__(self, parent, rennovering_vars): 
        super().__init__(master=parent, fg_color="transparent")
        self.pack(expand=True, fill='both')
        self.columnconfigure((0,1,2), weight=1)

        FrameColoum1 = ctk.CTkFrame(self)
        FrameColoum1.grid(row=0, sticky='new', columnspan=3 ,column=0, padx=5, pady=5)

class Renovering_plan_tab(ctk.CTkFrame): 
    def __init__(self, parent, rennovering_vars): 
        super().__init__(master=parent, fg_color="transparent")
        self.pack(expand=True, fill='both')
        self.columnconfigure((0,1,2), weight=1)

        FrameColoum1 = ctk.CTkFrame(self)
        FrameColoum1.grid(row=0, sticky='new', columnspan=3 ,column=0, padx=5, pady=5)

class Renovering_huskeliste_tab(ctk.CTkFrame): 
    def __init__(self, parent, rennovering_vars): 
        super().__init__(master=parent, fg_color="transparent")
        self.pack(expand=True, fill='both')
        self.columnconfigure((0,1,2), weight=1)

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