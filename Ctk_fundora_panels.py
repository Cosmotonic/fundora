# panels.py are not specific to any UI layout but are generic building blocks to avoid code repetition. 

import customtkinter as ctk
from Ctk_fundora_loanerValues import * 
from datetime import date

class Panel(ctk.CTkFrame):
    def __init__(self, parent): 
        super().__init__(master=parent, fg_color=DARK_GREY)
        self.pack_propagate(False)
        self.pack(fill='x', padx=4, pady=8)

       
class RenoveringsOpgavePanel(Panel): 
    def __init__(self, parent, delete_callback, UIDText='RenovationPanel', UID=1, columnLabels=['ekskludere','Opgave','Prio','Kommentar/Blokkere','Tidsforbrug','Pris','Slet']):
        super().__init__(parent=parent)
        # Order panel
        self.columnconfigure((0,1,2,3), weight=1)  # ← allow frame to expand in its parent
        self.rowconfigure(0, weight=1)

        # delete entire panel
        self.delete_callback = delete_callback

        # giver mit renovation panel et unikt ID, i stedet for at dict har hardcoded "badeværelse" som overrider hver gang jeg opetter et nyt. 
        self.uid = f"{UIDText}_{UID}" 

        self.vars = {}

        # init values 
        self.columnLabels = columnLabels
        self.current_row_index = 1  # Track row numbers

        # Lav hovedopgave 
        # Lav hovedframe til overordnet opgave
        self.OpgaveFrame = ctk.CTkFrame(self)
        self.OpgaveFrame.grid(row=0, sticky='new', columnspan=4 ,column=0, padx=5, pady=5)
        self.OpgaveFrame.columnconfigure((0, 1, 2, 3), weight=1)

        # Sæt Navn på opgave
        self.hovedopgave_navn_var = ctk.StringVar(value=f"Køkken etc.:") 
        self.OpgaveNavn_entry = ctk.CTkEntry(self.OpgaveFrame, textvariable=self.hovedopgave_navn_var, font=("Helvetica", 18, "bold"))
        self.OpgaveNavn_entry.grid(row = 0, column=0, sticky = 'ew', padx=5, pady=5)

        # Sæt dropdown ind Prioritet 
        self.priority_options = {"Skal gøres" :  {"color": "#16AD7E", "desc": "Skal gøres"},
                                 "Bør gøres"  :  {"color": "#fa0060", "desc": "Bør gøres"},
                                 "Kan gøres"  :  {"color": "#ca8300", "desc": "Kan gøres"}}
    
        self.hovedopgave_dropdown_var = ctk.StringVar(value="Skal gøres")

        self.dropdown = ctk.CTkOptionMenu(self.OpgaveFrame,
                                            variable=self.hovedopgave_dropdown_var,
                                            values=list(self.priority_options.keys()),
                                            command=self.update_dropdown_color)  # ← Hook here

        self.dropdown.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        # Inkluder i budget checkbox 
        self.inkluder_budget_var = ctk.BooleanVar(value=True)
        self.inkluder_budget_check = ctk.CTkCheckBox(self, variable=self.inkluder_budget_var, text="Inkluder i budget  ", fg_color= "#16AD7E", bg_color= "#09573E", hover_color= "#1CCC94" )
        self.inkluder_budget_check.grid(row=0, column=2, padx=(5,5), pady=5, sticky="w")

        # Tilføj opgave button
        self.tilføj_opgave_button = ctk.CTkButton(self.OpgaveFrame, 
                                            command=self.add_line,
                                            text="+ Tilføj opgave", 
                                            corner_radius=32, 
                                            hover_color="#0798EC", 
                                            fg_color='transparent', 
                                            border_color="#0077FF",  
                                            border_width=2, )  
               
        self.tilføj_opgave_button.grid(row = 0, column=3, padx=5, pady=5, columnspan=1, sticky = 'e')

        # Slet renovation button
        self.tilføj_opgave_button = ctk.CTkButton(self.OpgaveFrame, 
                                            command=self.delete_self,
                                            text="+ Slet Hele renovation", 
                                            corner_radius=32, 
                                            hover_color="#EC075F", 
                                            fg_color='transparent', 
                                            border_color="#C00040",  
                                            border_width=2 )  
               
        self.tilføj_opgave_button.grid(row = 0, column=3, padx=5, pady=5, columnspan=1, sticky = 'w')


        # Tilføj underopgaver
        # Tilføj ny frame til underopgaver
        self.underopgave_frame = ctk.CTkFrame(self)
        self.underopgave_frame.grid(row=1, column=0, padx=5, pady=5, columnspan=4, sticky='new')
        self.underopgave_frame.columnconfigure(tuple(range(12)), weight=1)

        # set column labels.
        ctk.CTkLabel(self.underopgave_frame, text=columnLabels[0]).grid(row=0, column=0, columnspan=1, padx=(10, 4), pady=2, sticky="w")
        ctk.CTkLabel(self.underopgave_frame, text=columnLabels[1]).grid(row=0, column=1, columnspan=2, sticky="ew",  padx=5, pady=5)
        ctk.CTkLabel(self.underopgave_frame, text=columnLabels[2]).grid(row=0, column=3, columnspan=1, sticky="ew",  padx=5, pady=5)
        ctk.CTkLabel(self.underopgave_frame, text=columnLabels[3]).grid(row=0, column=4, columnspan=6, sticky="ew",  padx=5, pady=5)
        ctk.CTkLabel(self.underopgave_frame, text=columnLabels[4]).grid(row=0, column=10,columnspan=2, sticky="ew",  padx=5, pady=5)
        ctk.CTkLabel(self.underopgave_frame, text=columnLabels[5]).grid(row=0, column=12,columnspan=3, sticky="ew",  padx=5, pady=5)
        ctk.CTkLabel(self.underopgave_frame, text=columnLabels[6]).grid(row=0, column=15,columnspan=1, sticky="ew",  padx=5, pady=5)

        # Total pris
        # OpgaveTotalPris = ctk.StringVar(value="100000")
        # self.total_pris = ctk.CTkEntry(self.OpgaveFrame, textvariable=OpgaveTotalPris)
        # self.total_pris.grid(row=99, column=3, sticky="e")

    def add_line(self, label_text="", checked=False, priority=None, comment=""):
        row = self.current_row_index
        self.rowconfigure(row, weight=0) 
        
        # Opret navne 
        var_chk     = ctk.BooleanVar(value=checked)
        var_str1    = ctk.StringVar(value=self.columnLabels[1])
        var_str2    = ctk.StringVar(value=self.columnLabels[2])
        var_str3    = ctk.StringVar(value=self.columnLabels[3])
        var_str4    = ctk.StringVar(value=self.columnLabels[4])
        var_str5    = ctk.StringVar(value=self.columnLabels[5])
        var_butStr  = ctk.StringVar(value=' - ')

        # Lav elements 
        checkbox = ctk.CTkCheckBox(self.underopgave_frame, text="", variable=var_chk)
        entry1 = ctk.CTkEntry(self.underopgave_frame, textvariable=var_str1)
        entry2 = ctk.CTkEntry(self.underopgave_frame, textvariable=var_str2)
        entry3 = ctk.CTkEntry(self.underopgave_frame, textvariable=var_str3)
        entry4 = ctk.CTkEntry(self.underopgave_frame, textvariable=var_str4)
        entry5 = ctk.CTkEntry(self.underopgave_frame, textvariable=var_str5)
        slet_but = ctk.CTkButton(self.underopgave_frame, textvariable=var_butStr, command=lambda r=row: self.slet_opgave(f"row_{r}")) # this current instanced row


        # Placer alt  
        checkbox.grid(row=row, column=0, columnspan=1, padx=5, pady=2, sticky="w")
        entry1.grid(row=row,   column=1, columnspan=2, sticky="ew", padx=5, pady=5)
        entry2.grid(row=row,   column=3, columnspan=1, sticky="ew", padx=5, pady=5)
        entry3.grid(row=row,   column=4, columnspan=6, sticky="ew", padx=5, pady=5)
        entry4.grid(row=row,   column=10,columnspan=2, sticky="ew", padx=5, pady=5)
        entry5.grid(row=row,   column=12,columnspan=3, sticky="ew", padx=5, pady=5)
        slet_but.grid(row=row, column=15,columnspan=1, sticky="ew", padx=5, pady=5)

        
        self.vars[f"row_{row}"] = {
            self.columnLabels[0]: checkbox,        # e.g. 'Ekskludere' checkbox
            self.columnLabels[1]: entry1,         # e.g. 'Opgave'
            self.columnLabels[2]: entry2,         # e.g. 'Prio'
            self.columnLabels[3]: entry3,         # e.g. 'Kommentar/Blokkere'
            self.columnLabels[4]: entry4,         # e.g. 'Tidsforbrug'
            self.columnLabels[5]: entry5,         # e.g. 'Pris'
            self.columnLabels[6]: slet_but,         # e.g. 'button'
        }

        self.current_row_index += 1

    def get_results(self):
        results = {}
        for i, data in enumerate(self.vars.values()): 
            # print (f'Var print::: {data}')
            task_name = data[self.columnLabels[1]].get().strip()  # 'Opgave'
            if not task_name:
                task_name = f"Opgave_{i+1}"
            key = f"{task_name}_{i+1}"  # Sikrer unikhed

            results[key] = {
                self.columnLabels[0]: data[self.columnLabels[0]].get(),  # Ekskludere
                self.columnLabels[1]: task_name,
                self.columnLabels[2]: data[self.columnLabels[2]].get(),  # 'Prio'
                self.columnLabels[3]: data[self.columnLabels[3]].get(),  # 'Kommentar/Blokkere'
                self.columnLabels[4]: data[self.columnLabels[4]].get(),  # 'Tidsforbrug'
                self.columnLabels[5]: data[self.columnLabels[5]].get(),  # 'Pris'
            }
        return results

    def load_data(self, data_dict):
        for task_name, values in data_dict.items():
            self.add_line(
                include=values.get(self.columnLabels[0], False),   # 'Ekskludere'
                opgave=task_name,                                  # 'Opgave'
                prio=values.get(self.columnLabels[2], ""),         # 'Prio'
                kommentar=values.get(self.columnLabels[3], ""),    # 'Kommentar/Blokkere'
                tid=values.get(self.columnLabels[4], ""),          # 'Tidsforbrug'
                pris=values.get(self.columnLabels[5], "")          # 'Pris'
            )

    def slet_opgave(self, row_id):
        if row_id in self.vars:
            print ("Fjern widgets fra UI")
            for widget in self.vars[row_id].values():
                if hasattr(widget, "grid_forget"):
                    widget.grid_forget()
                    widget.destroy()
            del self.vars[row_id]
     
    # drop down color change not setup yet. 
    def update_dropdown_color(self, selected_value):
        color = self.priority_options.get(selected_value, {}).get("color", "#cccccc")
        self.dropdown.configure(fg_color=color)
        
    def delete_self(self):
        if self.delete_callback:
            self.delete_callback(self)
    

class ForhandlingCheckPanel(Panel):
    def __init__(self, parent, checklist_data, priority_options, AddCustomLine=True, columnLabels=['1','2','3','4']):
        super().__init__(parent=parent)
        
        self.columnLabels = columnLabels
        self.vars = {}
        self.current_row_index = 1  # Track row numbers

        self.priority_options = priority_options 

        # set column labels.
        for index, i in enumerate(self.columnLabels):
            ctk.CTkLabel(self, text=i).grid(row=0, column=index, sticky='w', padx=5)

        # Indsæt alle eksempel linjer. 
        for label_text, data in checklist_data.items():
            priority_val = data.get("priority", list(self.priority_options.keys())[0])
            priority_var = ctk.StringVar(value=priority_val)

            self.add_line(
                label_text=label_text,
                checked=data.get("checked", False),
                priority=priority_var,
                comment=data.get("comment", "")
            )

        # Indsæt "+" button til at tilføje punkt
        if AddCustomLine: 
            add_button = ctk.CTkButton(
                self,
                text="+ Tilføj punkt",
                command=self.add_line,
                hover_color="#EC6E07", 
                fg_color='transparent', 
                border_color="#FF9100", 
                border_width=2
                )
            
            add_button.grid(row=999, column=1, columnspan=2, pady=(10, 5), padx=10, sticky="ew")

    def add_line(self, label_text="", checked=False, priority=None, comment=""):
        row = self.current_row_index
        self.rowconfigure(row, weight=0)

        var_chk = ctk.BooleanVar(value=checked)
        label_var = ctk.StringVar(value=label_text)
        comment_var = ctk.StringVar(value=comment)

        var_priority = priority or ctk.StringVar(value=list(self.priority_options.keys())[0])

        checkbox = ctk.CTkCheckBox(self, text="", variable=var_chk)
        checkbox.grid(row=row, column=0, padx=(10, 4), pady=2, sticky="w")

        label_entry = ctk.CTkEntry(self, textvariable=label_var)
        label_entry.grid(row=row, column=1, sticky="ew", padx=(0, 5))

        dropdown = ctk.CTkOptionMenu(
            self,
            variable=var_priority,
            values=list(self.priority_options.keys()),
            command=lambda val, v=var_priority: self.update_dropdown_color(v)
        )
        dropdown.grid(row=row, column=2, padx=(5, 5), sticky="ew")

        comment_entry = ctk.CTkEntry(self, textvariable=comment_var)
        comment_entry.grid(row=row, column=3, padx=(5, 10), sticky="ew")

        self.columnconfigure(3, weight=9)
        self.columnconfigure((1,2), weight=3)
        self.columnconfigure(0, weight=1)

        self.vars[f"row_{row}"] = {
            "checked": var_chk,
            "priority": var_priority,
            "comment": comment_var,
            "label": label_var,
            "dropdown_widget": dropdown,
            "priority_options": self.priority_options,
        }

        self.update_dropdown_color(var_priority)
        self.current_row_index += 1


    def update_dropdown_color(self, var):
        for item in self.vars.values():
            if item["priority"] == var:
                val = var.get()
                options = item.get("priority_options", {})
                color = options.get(val, {}).get("color", "#cccccc")  # fallback farve
                item["dropdown_widget"].configure(fg_color=color)

    def get_results(self):
        return {
            data["label"].get(): {
                "checked": data["checked"].get(),
                "priority": data["priority"].get(),
                "comment": data["comment"].get()
            }
            for data in self.vars.values()
        }

class BooleanInputPanel(Panel): 
    def __init__(self, parent, text, data_var): 
        super().__init__(parent=parent)

        #self.rowconfigure(0, weight=1)
        self.columnconfigure((0, 1), weight=1)

        # Label
        ctk.CTkLabel(self, text=text).grid(row=0, column=0, sticky='w', padx=5)

        # Switch (acts as boolean button)
        self.bool_switch = ctk.CTkSwitch(self, variable=data_var, text="Fra/TiL", fg_color="#3a3a3a")
        self.bool_switch.grid(row=0, column=1, sticky='e', padx=5, pady=5)

class SingleInputPanel(Panel): 
    def __init__(self, parent, text, data_var, readOnly = False, entry_sticky='e'): 
        super().__init__(parent=parent)

        readOption = 'normal'
        read_color = '#2b2b2b'
        if readOnly == True: 
            readOption = 'disabled'
            read_color ="#3a3a3a"

        self.rowconfigure((0,1),weight=1)
        self.columnconfigure((0), weight=1)
        self.columnconfigure((1), weight=1)

        ctk.CTkLabel(self, text = text).grid(row=0, column=0, sticky='w', padx=5) 
        self.SingleEntry = ctk.CTkEntry(self, textvariable= data_var, state=readOption, fg_color=read_color)
        self.SingleEntry.grid(row=0, sticky=entry_sticky, column=1,  columnspan=1, padx=5, pady=5)

class InlineDatePicker(Panel):
    def __init__(self, parent, text, date_vars):
        super().__init__(parent)

        self.rowconfigure((0,1,2,3),weight=1)
        self.columnconfigure((0,1,2,3), weight=1)

        # Variables
        self.day = date_vars[0]    # d
        self.month = date_vars[1]  # m
        self.year = date_vars[2]   # y
        self.output = date_vars[3] # DMY

        # Layout
        ctk.CTkLabel(self, text=text, font=("Arial", 14, "bold")).grid(row=0, column=0, sticky='w', columnspan=5, pady=10, padx=5)

        # Day dropdown
        ctk.CTkOptionMenu(self, variable=self.day, values=[str(i) for i in range(1, 32)], width=90).grid(row=1, column=0, padx=5, sticky='ew')
        ctk.CTkLabel(self, text="dag").grid(row=2, column=0, sticky='ew')

        # Month dropdown
        ctk.CTkOptionMenu(self, variable=self.month, values=[str(i) for i in range(1, 13)], width=90).grid(row=1, column=1, padx=5, sticky='ew')
        ctk.CTkLabel(self, text="måned").grid(row=2, column=1, sticky='ew')

        # Year dropdown
        years = [str(i) for i in range(1970, date.today().year + 1)]
        ctk.CTkOptionMenu(self, variable=self.year, values=years, width=90).grid(row=1, column=2, padx=5, sticky='ew')
        ctk.CTkLabel(self, text="år").grid(row=2, column=2, sticky='ew')

        # Submit button
        ctk.CTkButton(self, text="Vælg", command=self.set_date).grid(row=1, column=3, padx=10, sticky='ew')

        # Output field
        ctk.CTkEntry(self, textvariable=self.output, width=150, state="readonly").grid(row=0, column=3, padx=10, sticky='ew')

    def set_date(self):
        d = self.day.get()
        m = self.month.get()
        y = self.year.get()
        output_as_text = f"{d}/{m}/{y}"
        self.output.set(output_as_text)

class RadioInputPanel(Panel):
    def __init__(self, parent, text, data_var, perioder):
        super().__init__(parent=parent)
        
        self.rowconfigure((0,1), weight=1)
        self.columnconfigure((0,1), weight=1)
        
        self.data = data_var

        # Label
        ctk.CTkLabel(self, text=text).grid(row=0, column=0, sticky='w', padx=5)

        # Container for radio buttons
        radio_frame = ctk.CTkFrame(self, fg_color="transparent")
        radio_frame.grid(row=0, column=1, sticky='nsew', padx=5, pady=5)

        # Create radio buttons dynamically
        for idx, val in enumerate(perioder):
            btn = ctk.CTkRadioButton(radio_frame, text=str(val), variable=data_var, value=val, command= self.period_radio_update)
            btn.grid( sticky='e', row=0, column=idx, padx=1)

    def period_radio_update(self): 
        print (f"Lånperiode: {self.data.get()}") 

class FlexibleInputPanel(Panel): 
    def __init__(self, parent, name_var, value_var): 
        super().__init__(parent=parent)

        self.rowconfigure((0, 1), weight=1)
        self.columnconfigure((0, 1, 2), weight=1)

        # Felt til brugerens udgiftsnavn
        self.NameEntry = ctk.CTkEntry(self, placeholder_text="Navn på udgift", textvariable=name_var) # should be doublevar 
        self.NameEntry.grid(row=0, column=0, sticky='w', padx=5, pady=5)

        # Felt til beløb
        self.ValueEntry = ctk.CTkEntry(self, placeholder_text="Beløb", textvariable=value_var, fg_color='#2b2b2b')
        self.ValueEntry.grid(row=0, column=2, sticky='e', padx=5, pady=5)

class DoubleInputPanel(Panel): 
    def __init__(self, parent, text, field1, field2,  readOption_A='normal',  readOption_B='normal'): 
        super().__init__(parent=parent)

        self.columnconfigure(0, weight=1)  # ← allow frame to expand in its parent

        self.columnconfigure((0,1,2,3,4), weight=1)
        self.rowconfigure((0,1,2,3,4), weight=1)

        self.entry_a_var =  field1
        self.entry_b_var =  field2
        fgColorA = self.setBGColor(readOption_A)
        fgColorB = self.setBGColor(readOption_B)

        ctk.CTkLabel(self, text= text).grid(row=0, column=0, sticky='w', padx=5)
        self.entry_a    = ctk.CTkEntry(self, textvariable= self.entry_a_var, state=readOption_A, fg_color=fgColorA)
        self.entry_b    = ctk.CTkEntry(self, textvariable= self.entry_b_var, state=readOption_B, fg_color=fgColorB)

        self.entry_a.grid(row=0, sticky='ew',column=3,  columnspan=1, padx=5, pady=5)
        self.entry_b.grid(row=0, sticky='ew',column=4,  columnspan=2, padx=5, pady=5)

    def setBGColor(self, readState): 
        if readState == 'normal':
            read_color = '#2b2b2b'
        elif readState == 'disabled':    
            read_color ="#3a3a3a"

        return read_color

class xxInputPanel(Panel): 
    def __init__(self, parent, label_text, **input_fields): 
        super().__init__(parent=parent)

        # Configure layout
        self.columnconfigure(0, weight=1)  # label
        for i in range(1, len(input_fields) + 1):
            self.columnconfigure(i, weight=1)

        self.rowconfigure(0, weight=1)

        # Label
        ctk.CTkLabel(self, text=label_text).grid(row=0, column=0, sticky='w', padx=5)

        # Store entries if needed
        self.entries = {}

        for idx, (name, var) in enumerate(input_fields.items(), start=1):
            if hasattr(var, 'trace'):
                var.trace("w", lambda *args, n=name: self.on_change(n))

            entry = ctk.CTkEntry(self, textvariable=var)
            entry.grid(row=0, column=idx, sticky='ew', padx=5, pady=5)
            self.entries[name] = entry

    def on_change(self, name):
        print(f"Field '{name}' changed")

class ForhandlingsPanel(Panel): 
    def __init__(self, parent, text, entry1, entry2, udbudspris): 
        super().__init__(parent=parent)
 
        self.udbudspris = udbudspris
        self.columnconfigure(0, weight=1)  

        self.columnconfigure((0,1,2,3,4), weight=1)
        self.rowconfigure((0,1,2,3,4), weight=1)

        self.entry_a_var =  entry1
        self.entry_b_var =  entry2

        self.entry_a_var.trace("w", self.update_from_a)
        self.entry_b_var.trace("w", self.update_from_b)

        ctk.CTkLabel(self, text= text).grid(row=0, column=0, sticky='w', padx=5)
        self.entry_a    = ctk.CTkEntry(self, textvariable= self.entry_a_var)
        self.entry_b    = ctk.CTkEntry(self, textvariable= self.entry_b_var)

        self.entry_a.grid(row=0, sticky='ew',column=3,  columnspan=1, padx=5, pady=5)
        self.entry_b.grid(row=0, sticky='ew',column=4,  columnspan=2, padx=5, pady=5)

        self._suspend_trace = False

    def safe_int(self, value):
        try:
            if not value:
                return 0
            return int(float(value.strip()))
        except (ValueError, TypeError, AttributeError):
            return 0
        
    def update_from_a(self, *args): 
        if self._suspend_trace:
            return
        self._suspend_trace = True

        entry_val   = self.safe_int(self.entry_a_var.get())
        static_val  = self.safe_int(self.udbudspris.get())

        Value_for_b = round(((100-entry_val)/100) * static_val, 0)  

        self.entry_b_var.set(str(Value_for_b))
        self._suspend_trace = False

    def update_from_b(self, *args):
        if self._suspend_trace:
            return
        self._suspend_trace = True
        val         = self.safe_int(self.entry_b_var.get())
        static_val  = self.safe_int(self.udbudspris.get())
        Value_for_a = round(100 - (val / static_val * 100), 2)

        self.entry_a_var.set(str(Value_for_a))
        self._suspend_trace = False

class SliderPanel(Panel): 
    def __init__(self, parent, text1, text2, data_var, min_value, max_value, step_size=1, defaultValue=None): 
        super().__init__(parent=parent)

        self.data = data_var
        self.step_size = step_size  # Store for rounding
        self.default_value = defaultValue if defaultValue is not None else min_value

        self.rowconfigure((0, 1), weight=1)
        self.columnconfigure((0, 1), weight=1)

        self.name_label = ctk.CTkLabel(self, text=text1)
        self.name_label.grid(row=0, column=0, sticky='w', padx=5, pady=5)

        self.ValueEntry = ctk.CTkEntry(self, state='disabled', textvariable=self.data, fg_color='#3a3a3a')
        self.ValueEntry.grid(row=0, column=2, sticky='e', padx=5, pady=5)

        number_of_steps = max(1, int((max_value - min_value) / step_size))

        self.slider = ctk.CTkSlider(
            self,
            fg_color=FG_COLOR,
            from_=min_value,
            to=max_value,
            number_of_steps=number_of_steps,
            command=self.slider_changed
        )
        self.slider.grid(row=1, column=0, columnspan=3, sticky='ew', padx=5, pady=5)
        self.slider.set(self.default_value)
        self.data.set(round(self.default_value))  # Sync var with slider initially

    def slider_changed(self, value):
        # Snap to step size
        snapped = round(value / self.step_size) * self.step_size
        if self.data.get() != snapped:
            self.data.set(snapped)

class SegmentedPanel(Panel):
    def __init__(self, parent, text, data_var, options): 
        super().__init__(parent=parent)
        ctk.CTkLabel(self, text=text)
        segment = ctk.CTkSegmentedButton(self, variable = data_var, values=options)
        segment.pack(side='left',expand=True, fill='both', padx = 4, pady = 4)

class SwitchPanel(Panel):
    def __init__(self, parent, *args): # ((var, text), (var, text))
        super().__init__(parent=parent)    
        for var, text in args: 
            switch = ctk.CTkSwitch(self, text = text, variable = var, button_color=BLUE_COLOR, fg_color=FG_COLOR)
            switch.pack(side='left', expand = True, fill='both' ,  pady=5, padx=5)

class DropDownPanel(ctk.CTkOptionMenu):
    def __init__(self, parent, data_var, options): # ((var, text), (var, text))
        super().__init__(master=parent, 
                         values=options, 
                         fg_color=DARK_GREY, 
                         button_color= DROPDOWN_MAIN_COLOR, 
                         button_hover_color=DROPDOWN_HOVER_COLOR, 
                         dropdown_hover_color= DROPDOWN_HOVER_COLOR,
                         variable=data_var) 
        self.pack(fill='x', pady = 4, padx=4)

class CloseSection(ctk.CTkButton):
    def __init__(self, parent, close_func):
        super().__init__(
            master=parent, 
            text = 'X', 
            command = close_func, 
            text_color=WHITE, 
            fg_color='transparent', 
            width=40, 
            height=40, 
            corner_radius=0,
            hover_color=CLOSE_RED)
        
        self.place(relx = 0.99, rely = 0.01, anchor = 'ne')

# class meterPanel(ctk.)