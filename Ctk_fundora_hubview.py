
import customtkinter as ctk
from tkinter import filedialog, Canvas
from loanerValues import * 

class hubview(ctk.CTkFrame): 
    def __init__(self, parent, **menues): 
        super().__init__(master = parent)

        self.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Let hubview_frame stretch its grid cells
        self.grid_rowconfigure((0, 1), weight=1)
        self.grid_columnconfigure((0, 1), weight=1)

        self.frames = []

        # Add the menues (can be changed later)
        for idx, (name, func) in enumerate(menues.items()):
                row = idx // 2  
                col = idx % 2   

                frame = OpenSection(self, func, button_text=name.capitalize())
                frame.grid(row=row, column=col, padx=10, pady=10,  sticky="nsew")

                self.frames.append(frame)

class OpenSection(ctk.CTkFrame): 
    def __init__(self, parent, menu_section, button_text = 'Section X'): 
        super().__init__(master = parent)
        #self.grid(column = 0, columnspan = 2, row = 0, sticky = 'nsew')
        self.menu_func = menu_section 

        self.but1 = ctk.CTkButton(self, text = button_text, command = self.menu_func, corner_radius=32, hover_color="#006AC0")
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



