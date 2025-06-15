# panels.py are not specific to any UI layout but are generic building blocks to avoid code repetition. 

import customtkinter as ctk
from Ctk_fundora_loanerValues import * 
from datetime import date

class Panel(ctk.CTkFrame):
    def __init__(self, parent): 
        super().__init__(master=parent, fg_color=DARK_GREY)
        self.pack_propagate(False)
        self.pack(fill='x', padx=4, pady=8)

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

class ForhandlingCheckPanel(Panel):
    def __init__(self, parent, checklist_data):
        super().__init__(parent=parent)
        self.vars = {}
        self.current_row_index = 0  # Track row numbers

        self.priority_options = {
            "Vigtigt": {"color": "#236752", "desc": "Skal prioriteres"},
            "Bonus": {"color": "#1554c0", "desc": "Godt at få med"},
            "Ikke relevant": {"color": "#b71c62", "desc": "Springes over"}
        }

        # Create rows from initial data
        for label_text, data in checklist_data.items():
            self.add_line(
                label_text=label_text,
                checked=data.get("checked", False),
                priority=data.get("priority", "Vigtigt"),
                comment=data.get("comment", "")
            )

        # Add "+" button
        add_button = ctk.CTkButton(
            self,
            text="+ Tilføj punkt",
            fg_color="#f08c2e",  # Orange
            hover_color="#d37314",
            command=self.add_line
        )
        add_button.grid(row=999, column=0, columnspan=4, pady=(10, 0), padx=10, sticky="ew")

    def add_line(self, label_text="", checked=False, priority="Vigtigt", comment=""):
        row = self.current_row_index
        self.rowconfigure(row, weight=0)

        # Checkbox
        var_chk = ctk.BooleanVar(value=checked)
        checkbox = ctk.CTkCheckBox(self, text="", variable=var_chk)
        checkbox.grid(row=row, column=0, padx=(10, 4), pady=2, sticky="w")

        # Editable label
        label_var = ctk.StringVar(value=label_text)
        label_entry = ctk.CTkEntry(self, textvariable=label_var)
        label_entry.grid(row=row, column=1, sticky="ew", padx=(0, 5))

        # Priority dropdown
        var_priority = ctk.StringVar(value=priority)
        dropdown = ctk.CTkOptionMenu(
            self,
            variable=var_priority,
            values=list(self.priority_options.keys()),
            command=lambda val, v=var_priority: self.update_dropdown_color(v)
        )

        dropdown.grid(row=row, column=2, padx=(5, 5), sticky="ew")

        # Comment field
        comment_var = ctk.StringVar(value=comment)
        comment_entry = ctk.CTkEntry(self, textvariable=comment_var)
        comment_entry.grid(row=row, column=3, padx=(5, 10), sticky="ew")

        self.columnconfigure(3, weight=1)

        # Save reference
        key = f"row_{row}"
        self.vars[key] = {
            "checked": var_chk,
            "priority": var_priority,
            "comment": comment_var,
            "label": label_var,
            "dropdown_widget": dropdown,
            "priority_options": self.priority_options
        }

        self.update_dropdown_color(var_priority)
        self.current_row_index += 1

    def update_dropdown_color(self, var):
        for item in self.vars.values():
            if item["priority"] == var:
                val = var.get()
                color = item["priority_options"][val]["color"]
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
        self.columnconfigure(0, weight=1)  # ← allow frame to expand in its parent

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
        
    def update_from_a(self, *args): # % 
        if self._suspend_trace:
            return
        self._suspend_trace = True

        entry_val   = self.safe_int(self.entry_a_var.get())
        static_val  = self.safe_int(self.udbudspris.get())

        Value_for_b = round(((100-entry_val)/100) * static_val, 0)  
        print (f'value for B: {Value_for_b}')

        self.entry_b_var.set(str(Value_for_b))
        self._suspend_trace = False

    def update_from_b(self, *args):
        if self._suspend_trace:
            return
        self._suspend_trace = True
        val         = self.safe_int(self.entry_b_var.get())
        static_val  = self.safe_int(self.udbudspris.get())
        Value_for_a = round(100 - (val / static_val * 100), 2)
        #Value_for_a = round(((val/static_val) * -100 ) + 100, 2)
        print (f'value for A: {Value_for_a}')

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