
import customtkinter as ctk
from tkinter import filedialog, Canvas
from Ctk_fundora_loanerValues import * 

class hubview(ctk.CTkFrame): 
    def __init__(self, parent, importer_data_fra_db, eksporter_data_til_db, logout_callback, **menues): 
        super().__init__(master = parent)

        self.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Let hubview_frame stretch its grid cells
        self.frames = []

        # square menus
        if len(menues.items())== 4: 
            self.grid_rowconfigure((0, 1), weight=1)
            self.grid_columnconfigure((0, 1), weight=1)
            for idx, (name, func) in enumerate(menues.items()):
                    row = idx // 2  
                    col = idx % 2   

                    frame = OpenSection(self, func, button_text=name.upper())
                    frame.grid(row=row, column=col, padx=10, pady=10,  sticky="nsew")

                    self.frames.append(frame)
        
        # row of menus
        else: 
            self.grid_rowconfigure((0), weight=8)
            self.grid_rowconfigure((1), weight=2)
            self.grid_columnconfigure((0,1,2), weight=1)
            for idx, (name, func) in enumerate(menues.items()):
                    frame = OpenSection(self, func, button_text=name.upper())
                    frame.grid(row=0, column=idx, padx=10, pady=10,  sticky="nsew")

                    self.frames.append(frame)
            print ('Not 4 panels, but  %s ' % idx )


        # make logout button
        self.lotout_button = ctk.CTkButton(self, text="Log out", hover_color="#EC006E", 
                                 fg_color='transparent', 
                                 border_color="#BE0059", 
                                 border_width=2,
                                 command=logout_callback)
        
        self.lotout_button.grid(row=2, column=1, padx=10, pady=10, sticky="nsew")

        # Database Temp UI
        # Eksporter til database 
        self.export_data_button = ctk.CTkButton(self, 
                                            text="Eksporter til Database MySQL", 
                                            corner_radius=32, 
                                            hover_color="#07ECA0", 
                                            fg_color='transparent', 
                                            border_color="#00C479", 
                                            border_width=2,
                                            command=eksporter_data_til_db )
                    
        self.export_data_button.grid(row = 4, column=0, columnspan=1)
        # Importer til database 
        self.import_data_button = ctk.CTkButton(self, 
                                            text="Importer til Database MySQL", 
                                            corner_radius=32, 
                                            hover_color="#9C009C", 
                                            fg_color='transparent', 
                                            border_color="#7E0069", 
                                            border_width=2, 
                                            command=importer_data_fra_db )
                    
        self.import_data_button.grid(row = 4, column=1, columnspan=1)





class OpenSection(ctk.CTkFrame): 
    def __init__(self, parent, menu_section, button_text = 'Section X'): 
        super().__init__(master = parent)
        #self.grid(column = 0, columnspan = 2, row = 0, sticky = 'nsew')
        self.menu_func = menu_section 

        self.but1 = ctk.CTkButton(self, text = button_text, command = self.menu_func, corner_radius=32, hover_color="#006AC0", font=("Helvetica", 18, "bold"))
        self.but1.pack(expand=True, fill='both')

    def open_dialog(self):
        path = filedialog.askopenfile().name
        self.import_func(path)

class ImageOutput(Canvas):
    def __init__(self, parent, resize_image):
        super().__init__(master=parent, background=BACKGROUND_COLOR, bd = 0, highlightthickness= 0, relief='ridge')
        self.grid(row=0, column=1, sticky='nsew', padx=10, pady=10)
        self.bind('<Configure>', resize_image) # meaning an event is triggered everytime we resize the canvas. 

class CloseOutput(ctk.CTkButton):
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



