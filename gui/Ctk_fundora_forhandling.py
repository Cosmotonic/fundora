import customtkinter as ctk
from components.Ctk_fundora_panels import SingleInputPanel, ForhandlingsPanel, SliderPanel, DoubleInputPanel, ForhandlingCheckPanel
import backend.Ctk_fundora_exportPDF as export 
from Ctk_fundora_loanerValues import *


class Forhandling(ctk.CTkTabview): 
    def __init__(self, parent, forhandlings_vars): 
        super().__init__(master = parent, fg_color=WHITE,
                         segmented_button_selected_color=PURPLE, 
                         segmented_button_selected_hover_color=LIGHT_PURPLE, 
                         segmented_button_unselected_hover_color=LIGHT_PURPLE, text_color=WHITE, border_color= ORANGE)
        
        self.grid(row=0, column=0, sticky='nsew', pady=10, padx=10)

        self.add("Konsessiv Forhandling")
        self.add("Argumentation")
        self.add("Løsøre")
        self.add("Eksport")
        
        mainApp = parent 

        Ackerman_tab(self.tab("Konsessiv Forhandling"), forhandlings_vars)
        
        self.argument_tab = Argument_tab(self.tab("Argumentation"), mainApp, mainApp.forhandlings_argumenter_dict) 
        self.løsøre_tab   = Løsøre_tab(self.tab("Løsøre"), mainApp, mainApp.forhandlings_løsøre_dict)
        self.eksport_tab = Eksport_tab(self.tab("Eksport"), forhandlings_vars, argumenter_getter_func=self.argument_tab.get_results, løsøre_getter_func=self.løsøre_tab.get_results)


class Ackerman_tab(ctk.CTkFrame): 
    def __init__(self, parent, forhandlings_vars): 
        super().__init__(master=parent, fg_color=WHITE)#"transparent")
        self.pack(expand=True, fill='both')
        self.columnconfigure((0,1,2), weight=1)

        FrameColoum1 = ctk.CTkFrame(self, fg_color=WHITE, border_width=2, border_color=DARK_GREY)
        FrameColoum1.grid(row=0, sticky='new', columnspan=3 ,column=0, padx=5, pady=5)
        SingleInputPanel(FrameColoum1, "Udbudspris", forhandlings_vars["udbudspris"])

        # beregn forventet besparing i procent
        ForhandlingsPanel(FrameColoum1, "Forventet procent afslag & max købspris",  forhandlings_vars['forventet_procent'], forhandlings_vars['forventet_pris'], forhandlings_vars['udbudspris'])
        SliderPanel(FrameColoum1, "Koncessiv forhandlingsaggressivitet", "0", forhandlings_vars["aggressivitet"], 1, 3, defaultValue=1, step_size=1)
        
        outputFrame = ctk.CTkFrame(self, fg_color=WHITE,  border_width=2, border_color=DARK_GREY)
        outputFrame.grid(row=1, sticky='new', columnspan=3 ,column=0, padx=5, pady=5)
        
        DoubleInputPanel(outputFrame, "1. Forhandlingsbud: ", forhandlings_vars['runde1_procent'], forhandlings_vars['runde1_pris'], readOption_A='disabled',  readOption_B='disabled') 
        DoubleInputPanel(outputFrame, "2. Forhandlingsbud: ", forhandlings_vars['runde2_procent'], forhandlings_vars['runde2_pris'], readOption_A='disabled',  readOption_B='disabled') 
        DoubleInputPanel(outputFrame, "3. Forhandlingsbud: ", forhandlings_vars['runde3_procent'], forhandlings_vars['runde3_pris'], readOption_A='disabled',  readOption_B='disabled') 
        DoubleInputPanel(outputFrame, "4. Forhandlingsbud: ", forhandlings_vars['runde4_procent'], forhandlings_vars['runde4_pris'], readOption_A='disabled',  readOption_B='disabled') 
   
class Argument_tab(ctk.CTkFrame): 
    def __init__(self, parent, mainApp, forhandlings_Argumenter_dict): 
        super().__init__(master=parent, fg_color=WHITE)
        self.pack(expand=True, fill='both')

        self.columnconfigure(0, weight=1)
        #self.rowconfigure(0, weight=1)

        FrameColoum1 = ctk.CTkFrame(self, fg_color=WHITE,  border_width=2, border_color=DARK_GREY)
        FrameColoum1.grid(row=0, sticky='new', column=0, padx=5, pady=5)

        # argumenter
        self.priority_options = {"Fordel": {"color": "#236752", "desc": "Skal prioriteres"},
                                 "Ulempe":  {"color": "#b71c62", "desc": "Springes over"}}
        
        # Refactor til var for bedre PDF eksport. example: forhandlings_var['Arg_label_Column0'] 
        self.columnLabels=['Til PDF', 'Argument', 'Fra købers perspektiv', 'Købers argumentation'] 

        self.panel = ForhandlingCheckPanel(mainApp, parent=FrameColoum1,ref_dict=forhandlings_Argumenter_dict, 
                                           priority_options=self.priority_options, AddCustomLine=True, columnLabels=self.columnLabels, 
                                           inspiration_ref_dict=mainApp.forhandlings_argumenter_inspiration_dict) 
        self.panel.pack(fill="both", expand=True)

        mainApp.all_UGC_update_functions["argument_update_dict"] = self.panel.update_ref_dict

    def get_results(self):
        resultater = self.panel.get_results()
        print ("Entered Get Results on aguments")

        return resultater


class Løsøre_tab(ctk.CTkFrame): 
    def __init__(self, parent, mainApp, forhandlings_løsøre_dict): 
        super().__init__(master=parent, fg_color=WHITE)
        self.pack(expand=True, fill='both')

        self.columnconfigure(0, weight=1)
        #self.rowconfigure(0, weight=1)

        FrameColoum1 = ctk.CTkFrame(self, fg_color=WHITE)
        FrameColoum1.grid(row=0, sticky='new', column=0, padx=5, pady=5)

        # interesse 
        self.priority_options1 = {  "Vigtigt": {"color": "#236752", "desc": "Skal prioriteres"},
                                    "Bonus": {"color": "#1554c0", "desc": "Godt at få med"},
                                    "Ikke relevant": {"color": "#b71c62", "desc": "Springes over"}}
        
        self.columnLabels=['TIL PDF', 'Løsøre', 'Vigtighed', 'Egne noter'] 

        self.panel = ForhandlingCheckPanel(mainApp, parent=FrameColoum1, ref_dict=forhandlings_løsøre_dict, 
                                           priority_options=self.priority_options1, columnLabels=self.columnLabels, 
                                           inspiration_ref_dict=mainApp.forhandlings_løsøre_inspiration_dict) 
        self.panel.pack(fill="both", expand=True)

        mainApp.all_UGC_update_functions["losore_update_dict"] = self.panel.update_ref_dict

        #print_button = ctk.CTkButton(self, text="Print resultater", command=self.get_results)
        #print_button.grid(row=1, column=0, pady=10, padx=10, sticky="new")

    def get_results(self):
        resultater = self.panel.get_results()
        print ("Entered Get Results on Løsøre")
        return resultater

    #def get_checklist_results(self):
    #    return self.panel.get_results()


class Eksport_tab(ctk.CTkFrame): 
    def __init__(self, parent, forhandlings_vars,  argumenter_getter_func, løsøre_getter_func): # vi skal ikke have init dicts med ind her fordi vi skal generer dem hver gang vi trykker eksport, derfor skal de laves i panel. 
        super().__init__(master=parent, fg_color=WHITE)
        self.pack(expand=True, fill='both')

        # getter funktioner
        self.argumenter_getter_func = argumenter_getter_func
        self.løsøre_getter_func     = løsøre_getter_func

        self.columnconfigure((0, 1), weight=1)

        # layout
        person_frame1 = ctk.CTkFrame(self, fg_color=WHITE)
        person_frame1.grid(row=1, column=0, columnspan=1, padx=5, pady=5, sticky='new')
        person_frame2 = ctk.CTkFrame(self, fg_color=WHITE)
        person_frame2.grid(row=1, column=1, columnspan=1, padx=5, pady=5, sticky='new')

        # Beregning 
        self.beregn_button = ctk.CTkButton(self, 
                                            text="Eksporter PDF - bug: exportere kun den oprindelige dict", 
                                            corner_radius=32, 
                                            hover_color=HIGHTLIGHT_ORANGE, 
                                            fg_color=DARK_ORANGE, 
                                            border_color=DARK_ORANGE, 
                                            text_color=WHITE_TEXT_COLOR,
                                            font=("Helvetica", 14, "bold"),
                                            border_width=2,
                                            command=lambda: export.Eksport_forhandling_PDF(forhandlings_vars, self.get_all_results()))

        self.beregn_button.grid(row = 3, column=0, columnspan=2)

    def get_all_results(self):
        #print(self.argumenter_getter_func())  
        #print(self.løsøre_getter_func())
        return {
            "argumenter": self.argumenter_getter_func(),
            "losore": self.løsøre_getter_func()
        }
