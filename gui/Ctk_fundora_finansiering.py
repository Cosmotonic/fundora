# Ctk_fundora_finansiering

import customtkinter as ctk
import backend.Ctk_fundora_exportPDF as export 

from components.Ctk_fundora_panels import ( SingleInputPanel, FlexibleInputPanel, ForhandlingsPanel, DoubleInputPanel, SliderPanel, 
                                RadioInputPanel, BooleanInputPanel, xxInputPanel, InlineDatePicker, CloseSection )

from Ctk_fundora_loanerValues import *
import backend.Ctk_fundora_math_lib as fuMath 

class Finansering(ctk.CTkTabview): 
    def __init__(self, parent, finansiering_vars, udgift_vars, fremtid_vars, person_info_vars, mainApp): 
        super().__init__(master = parent, fg_color=WHITE)
        self.grid(row=0, column=0, sticky='nsew', pady=10, padx=10)

        #self.add("Intro")
        self.add("Finansiering")
        self.add("Bolig Udgift")
        self.add("Fremtidig Økonomi")
        self.add("Person Oplysninger & Eksport")

        #Intro_tab(self.tab("Intro"))
        Laane_Evne_tab(self.tab("Finansiering"), finansiering_vars)
        Bolig_Udgift_tab(self.tab("Bolig Udgift"), finansiering_vars, udgift_vars)
        Fremtidig_Oekonomi_tab(self.tab("Fremtidig Økonomi"), finansiering_vars, udgift_vars, fremtid_vars, person_info_vars, mainApp)
        Eksport_tab(self.tab("Person Oplysninger & Eksport"),  finansiering_vars, udgift_vars, fremtid_vars, person_info_vars, mainApp)
        
class Intro_tab(ctk.CTkFrame): 
    def __init__(self, parent): 
        super().__init__(master=parent, fg_color="transparent")
        self.pack(expand=True, fill='both')
        
class Laane_Evne_tab(ctk.CTkFrame): 
    def __init__(self, parent, Finansiering_vars): 
        super().__init__(master=parent, fg_color="transparent")
        self.pack(expand=True, fill='both')

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        #self.rowconfigure(0, weight=1)
      
        person1Frame = ctk.CTkFrame(self)#  fg_color=LIGHT_ORANGE)
        person1Frame.grid(row=0, sticky='new',column=0, padx=5, pady=5)

        person2Frame = ctk.CTkFrame(self)#  fg_color=LIGHT_ORANGE)
        person2Frame.grid(row=0, sticky='new',column=1, padx=5, pady=5)

        ctk.CTkLabel(person1Frame, text="1. Person ").pack()

        # person 1 using panels. 
        SingleInputPanel(person1Frame, "Løn før skat: ", Finansiering_vars["indtaegt_1"])
        SingleInputPanel(person1Frame, "Pension %: ", Finansiering_vars["pension_1"])
        SingleInputPanel(person1Frame, "Opsparring: ", Finansiering_vars["opsparring_1"])
        SingleInputPanel(person1Frame, "Gæld: ", Finansiering_vars["gaeld_1"])
        
        ctk.CTkLabel(person2Frame, text="2. Person ").pack()
        
        # person 2 using panels. 
        SingleInputPanel(person2Frame, "Løn før skat: ", Finansiering_vars["indtaegt_2"])
        SingleInputPanel(person2Frame, "Pension %: ", Finansiering_vars["pension_2"])
        SingleInputPanel(person2Frame, "Opsparring: ", Finansiering_vars["opsparring_2"])
        SingleInputPanel(person2Frame, "Gæld: ", Finansiering_vars["gaeld_2"])

        # Beregning 
        self.beregn_button = ctk.CTkButton(self, 
                                           text="Beregn", 
                                           command=lambda: fuMath.udregn_Indkomst(Finansiering_vars), 
                                           corner_radius=32, 
                                           hover_color=LIGHT_PURPLE, 
                                           fg_color=PURPLE, 
                                           border_color=PURPLE, 
                                           text_color=WHITE_TEXT_COLOR,
                                           border_width=2)

        self.beregn_button.grid(row = 2, column=0, columnspan=2)#, stick='ew')#, padx = 5, pady=5)# style="Calculate.TButton")  style = "primary"    

        output_frame = ctk.CTkFrame(self)#  fg_color=LIGHT_ORANGE)
        output_frame.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky='new')

        # Output values 
        SingleInputPanel(output_frame, "Samlet indtægt før skat: ", Finansiering_vars["samlet_indtaegt"], readOnly=True)
        SingleInputPanel(output_frame, "Max Lånfaktor (Indtægter x 4 + opsparing - gæld): ", Finansiering_vars["max_laan"], readOnly=True)
        SingleInputPanel(output_frame, "Person 1. Ca. Løn efter skat: ", Finansiering_vars["lon_efter_skat1"], readOnly=True)
        SingleInputPanel(output_frame, "Person 2. Ca. Løn efter skat: ", Finansiering_vars["lon_efter_skat2"], readOnly=True)
        SingleInputPanel(output_frame, "Samlet indtægt efter skat: ", Finansiering_vars["samlet_efter_skat"], readOnly=True)

        
class Bolig_Udgift_tab(ctk.CTkFrame): 
    def __init__(self, parent, finansiering_vars, udgift_vars): 
        super().__init__(master=parent, fg_color="transparent")
        self.pack(expand=True, fill='both')
        
        #self.rowconfigure((0,1),weight=1)
        self.columnconfigure((0,1,2), weight=1)
      
        FrameColoum1 = ctk.CTkFrame(self)
        FrameColoum1.grid(row=0, sticky='new',column=0, padx=5, pady=5)
        FrameColoum2 = ctk.CTkFrame(self)
        FrameColoum2.grid(row=0, sticky='new',column=1, padx=5, pady=5)
        FrameColoum3 = ctk.CTkFrame(self)
        FrameColoum3.grid(row=0, sticky='new',column=2, padx=5, pady=5)

        SingleInputPanel(FrameColoum1, "Ejerudgift: (Ejendomsværdiskat, fællesudg, osv. ) ",            udgift_vars["bolig_udgift"])
        SingleInputPanel(FrameColoum1, "Forbrug: (El, vand, varme, gas)",                               udgift_vars["forbrug"])
        SingleInputPanel(FrameColoum1, "Mad dagligvare: (Indkøb, husholdning)",                         udgift_vars["mad_dagligvare"])
        FlexibleInputPanel(FrameColoum1, udgift_vars["flex_udgift_string1"],                            udgift_vars["flex_udgift_var1"])

        SingleInputPanel(FrameColoum2, "Transport: (Bil, brændstof, offentlig transport)",              udgift_vars["transport"])
        SingleInputPanel(FrameColoum2, "Forsikringer: (Indbo, ulykke, bil, rejseforsikring)",           udgift_vars["forsikringer"])
        SingleInputPanel(FrameColoum2, "Telefon, internet og medier: (Mobil, bredbånd, streamingtjenester)",  udgift_vars["telefon_int_medie"])
        FlexibleInputPanel(FrameColoum2, udgift_vars["flex_udgift_string2"],                              udgift_vars["flex_udgift_var2"])

        SingleInputPanel(FrameColoum3, "Personlig pleje og toej: (Frisør, tøj, sko, personlig pleje)",  udgift_vars["personlig_pleje_toej"])
        SingleInputPanel(FrameColoum3, "Fritid og fornoejelser: (Fitness, biograf, hobbyer)",           udgift_vars["fritid_fornoejelser"])
        SingleInputPanel(FrameColoum3, "Pasning og fritidsaktiv: (Institution, SFO, sport)",            udgift_vars["pasning_fritidsaktiv"])
        FlexibleInputPanel(FrameColoum3, udgift_vars["flex_udgift_string3"],                            udgift_vars["flex_udgift_var3"])

        slider_frame = ctk.CTkFrame(self)
        slider_frame.grid(row=1, column=0, columnspan=3, padx=5, pady=5, sticky='new')
        SliderPanel(slider_frame, "Forventet købspris", "0", udgift_vars["forventet_pris"], 0, 10_000_000, defaultValue=5_000_000, step_size=12500)

        # Output values 
        output_frame = ctk.CTkFrame(self)
        output_frame.grid(row=2, column=0, columnspan=3, padx=5, pady=5, sticky='new')

        SingleInputPanel(output_frame, "Gældsfaktor: ",             udgift_vars["gaeldsfaktor"], readOnly=True)
        SingleInputPanel(output_frame, "Banklån: ",                 udgift_vars["banklaan"], readOnly=True)
        SingleInputPanel(output_frame, "Realkreditlån: ",           udgift_vars["realkreditlaan"], readOnly=True)
        SingleInputPanel(output_frame, "Samlet lån: ",              udgift_vars["samlet_laan"], readOnly=True)
        SingleInputPanel(output_frame, "Faste udgifter: ",          udgift_vars["alle_faste_udgifter"], readOnly=True)
        
        # Beregning 
        self.beregn_button = ctk.CTkButton(self, 
                                           text="Beregn", 
                                           command=lambda: fuMath.udregn_Bolig_Udgift_output(finansiering_vars, udgift_vars),
                                           corner_radius=32, 
                                           hover_color=LIGHT_PURPLE, 
                                           fg_color=PURPLE, 
                                           border_color=PURPLE, 
                                           text_color=WHITE_TEXT_COLOR,
                                           border_width=2)
        
        self.beregn_button.grid(row = 3, column=1, columnspan=1)#, stick='ew')#, padx = 5, pady=5)# style="Calculate.TButton")  style = "primary"    

class Fremtidig_Oekonomi_tab(ctk.CTkFrame): 
    def __init__(self, parent, finansiering_vars, udgift_vars, fremtid_vars, person_info_vars, mainApp): 
        super().__init__(master=parent, fg_color="transparent")
        self.pack(expand=True, fill='both')
        
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
      
        FrameColoum1 = ctk.CTkFrame(self)
        FrameColoum1.grid(row=1, column=0, sticky='new', padx=5, pady=5)
        FrameColoum2 = ctk.CTkFrame(self)
        FrameColoum2.grid(row=1, column=1, sticky='new', padx=5, pady=5)

        # real loan
        real_label = ctk.CTkLabel(self, text='Realkredit Lån')
        real_label.grid(row=0, column=0, sticky='new', padx=5, pady=5)
        SingleInputPanel(   FrameColoum1, "Realkredit Nominel Rente:",   fremtid_vars["realkredit_nominel"])
        SingleInputPanel(   FrameColoum1, "Realkredit Bidragssats:",     fremtid_vars["realkredit_bidragssats"])
        SingleInputPanel(   FrameColoum1, "Realkredit Terminer:",        fremtid_vars["realkredit_terminer"])
        RadioInputPanel(    FrameColoum1, "Realkredit Låneperiode (år):",fremtid_vars["realkredit_laaneperiode"], [5, 10, 15, 20, 30])
        BooleanInputPanel(  FrameColoum1, "10 Års Afdragsfrihed", fremtid_vars["afdragsfri"])

        # bank loan
        bank_label = ctk.CTkLabel(self, text='Bank Lån')
        bank_label.grid(row=0, column=1, sticky='new', padx=5, pady=5)
        SingleInputPanel(   FrameColoum2, "Bank Nominel Rente:",   fremtid_vars["bank_nominel"])
        SingleInputPanel(   FrameColoum2, "Bank Terminer:",        fremtid_vars["bank_terminer"])
        RadioInputPanel(    FrameColoum2, "Bank Låneperiode (år):",fremtid_vars["bank_laaneperiode"], [5, 10, 15, 20, 30])

        # Output values
        output_frame1 = ctk.CTkFrame(self)
        output_frame1.grid(row=2, column=0, columnspan=1, padx=5, pady=5, sticky='new')
        output_frame2 = ctk.CTkFrame(self)
        output_frame2.grid(row=2, column=1, columnspan=1, padx=5, pady=5, sticky='new')

        SingleInputPanel(output_frame1, "Rente Betaling: ",              fremtid_vars["rente_betaling"], readOnly=True)
        SingleInputPanel(output_frame1, "Rente Afdrag: ",                fremtid_vars["rente_afdrag"], readOnly=True)
        SingleInputPanel(output_frame1, "Rentefradrag: ",                fremtid_vars["rentefradrag"], readOnly=True)
        SingleInputPanel(output_frame1, "Rentefradrag %: ",              fremtid_vars["rentefradrag_procent"], readOnly=True)
        SingleInputPanel(output_frame2, "Samlet Ydelse: ",               fremtid_vars["samlet_ydelse"], readOnly=True)
        SingleInputPanel(output_frame2, "Faste udgifter: ",              fremtid_vars["fast_udgifter"], readOnly=True)
        SingleInputPanel(output_frame2, "Faster Udgifter plus Ydelse: ", fremtid_vars["fast_udgifter_inkl_ydelser"], readOnly=True)

        output_frame3 = ctk.CTkFrame(self)
        output_frame3.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky='new')

        SingleInputPanel(output_frame3, "Rådighedsbeløb: ",             fremtid_vars["raadighedsbeloeb"], readOnly=True)
        
        # Beregning
        self.beregn_button = ctk.CTkButton(self, 
                                           text="Beregn", 
                                           command=lambda: fuMath.udregn_fremtidig_økonomi(finansiering_vars, udgift_vars, fremtid_vars, person_info_vars, mainApp),
                                           corner_radius=32, 
                                           hover_color=LIGHT_PURPLE, 
                                           fg_color=PURPLE, 
                                           border_color=PURPLE, 
                                           text_color=WHITE_TEXT_COLOR,
                                           border_width=2)
        
 
        self.beregn_button.grid(row = 4, column=0, columnspan=2)

class Eksport_tab(ctk.CTkFrame): 
    def __init__(self, parent, finansiering_vars, udgift_vars, fremtid_vars, person_info_vars, mainApp): 
        super().__init__(master=parent, fg_color="transparent")
        self.pack(expand=True, fill='both')

        self.logged_in_email = mainApp.logged_in_email
        self.person_info_vars   = person_info_vars
        self.finansiering_vars  = finansiering_vars
        self.udgift_vars        = udgift_vars
        self.fremtid_vars       = fremtid_vars
        self.columnconfigure((0, 1), weight=1)

        # layout
        person_frame1 = ctk.CTkFrame(self)
        person_frame1.grid(row=1, column=0, columnspan=1, padx=5, pady=5, sticky='new')
        person_frame2 = ctk.CTkFrame(self)
        person_frame2.grid(row=1, column=1, columnspan=1, padx=5, pady=5, sticky='new')
        
        # Personlig information 1st person 
        person1_label = ctk.CTkLabel(self, text='1. Person')
        person1_label.grid(row=0, column=0, columnspan=1, padx=5, pady=5, sticky='new')
        DoubleInputPanel(person_frame1, "Navn: ", person_info_vars['Fornavn1'], person_info_vars['Efternavn1'])
        xxInputPanel    (person_frame1, "Adresse: ", field1=person_info_vars['adresse_vej1'],field2=person_info_vars['adresse_postnr1'],field3=person_info_vars['adresse_by1'])
        InlineDatePicker(person_frame1, "Fødselsdato", [person_info_vars['fodselsdag_dag1'], person_info_vars['fodselsdag_maaned1'], person_info_vars['fodselsdag_aar1'], person_info_vars['dato_dmo1']])
        SingleInputPanel(person_frame1, "Telefon: ",              person_info_vars["telefon1"], entry_sticky='ew')
        SingleInputPanel(person_frame1, "E-mail: ",               person_info_vars["mail1"],    entry_sticky='ew')

        # Personlig information 1st person 
        person2_label = ctk.CTkLabel(self, text='2. Person')
        person2_label.grid(row=0, column=1, columnspan=1, padx=5, pady=5, sticky='new')
        DoubleInputPanel(person_frame2, "Navn: ", person_info_vars['Fornavn2'], person_info_vars['Efternavn2'])
        xxInputPanel    (person_frame2, "Adresse: ", field1=person_info_vars['adresse_vej2'],field2=person_info_vars['adresse_postnr2'],field3=person_info_vars['adresse_by2'])
        InlineDatePicker(person_frame2, "Fødselsdato", [person_info_vars['fodselsdag_dag2'], person_info_vars['fodselsdag_maaned2'], person_info_vars['fodselsdag_aar2'], person_info_vars['dato_dmo2']])
        SingleInputPanel(person_frame2, "Telefon: ",              person_info_vars["telefon2"], entry_sticky='ew')
        SingleInputPanel(person_frame2, "E-mail: ",               person_info_vars["mail2"],entry_sticky='ew')

        Bolig_frame1 = ctk.CTkFrame(self)
        Bolig_frame1.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky='new')

        SingleInputPanel(Bolig_frame1, "Bolig Navn: ",     person_info_vars["ny_adresse_vej"], entry_sticky='ew')
        SingleInputPanel(Bolig_frame1, "Link til bolig: ", person_info_vars["link_til_ny_adresse"], entry_sticky='ew')

        # eksport 
        self.eksporter_button = ctk.CTkButton(self, 
                                            text="button_text", 
                                            corner_radius=32, 
                                            hover_color=HIGHTLIGHT_ORANGE, 
                                            fg_color=ORANGE, 
                                            border_color=DARK_ORANGE, 
                                            text_color=WHITE_TEXT_COLOR,
                                            font=("Helvetica", 14, "bold"),
                                            border_width=2, ) # command=lambda: export.Export_finansiering_PDF(self.set_export_values, mainApp, finansiering_vars, udgift_vars, fremtid_vars, person_info_vars))
                    
        self.eksporter_button.grid(row = 3, column=0, columnspan=2, pady=10)
        
        # set button text 
        self.upgrade_or_export()
        role = self.person_info_vars["user_role"].get()
        print (f"USER ROLE {role}")

    def upgrade_or_export(self):
        if self.person_info_vars["user_role"].get() == "premium":
            self.eksporter_button.configure(
                text="👑 Premium PDF Eksport",
                state="normal",  
                command=lambda: export.Export_finansiering_PDF(
                                    self.set_export_values, self.master, 
                                    self.finansiering_vars,
                                    self.udgift_vars, 
                                    self.fremtid_vars, 
                                    self.person_info_vars))
                
        else:
            self.eksporter_button.configure(
                text="Opgrader til 👑 Premium for PDF Eksport",
                state="normal",
                command=self.go_to_payment)
            
                
    def go_to_payment(self):      
        
        import webbrowser
        webbrowser.open("https://buy.stripe.com/test_cNi4gz1JJcXH93O6Rvawo00")    
 
    def set_export_values(self): 
        # Tracking event jeg vil bruge senere som bliver ført over til anden fuction. Obj program for life. 

        print (" ")
        #print (f"adresse before set: {self.person_info_vars['adresse_vej1'].get()}")
