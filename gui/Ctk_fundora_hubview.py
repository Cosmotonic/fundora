
import customtkinter as ctk
import sys

from pathlib import Path
from customtkinter import CTkImage
from tkinter import filedialog, Canvas
from components.Ctk_fundora_loanerValues import * 
from PIL import Image

class hubview(ctk.CTkFrame): 
    def __init__(self, parent, logout_callback, **menues): 
        super().__init__(master = parent, fg_color=WHITE)
        self.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # Let hubview_frame stretch its grid cells
        self.frames = []

        # square menus
        if len(menues.items())== 4: 
            self.grid_rowconfigure((0, 1), weight=1)
            self.grid_columnconfigure((0, 1), weight=1)
            for idx, (name, func) in enumerate(menues.items()):
                    row = idx // 2  
                    col = idx % 2   
                    frame = OpenSection(self, func, button_text=name.upper(), imagePath="")
                    frame.grid(row=row, column=col, padx=10, pady=10,  sticky="nsew")

                    self.frames.append(frame)
        
        # row of menus
        else: 
            hubframe = ctk.CTkFrame(self, fg_color=WHITE)

            hubframe.grid(row=0, column=0, sticky="nsew")
            hubframe.grid_rowconfigure((0), weight=1)
            hubframe.grid_rowconfigure((1), weight=7)
            hubframe.grid_rowconfigure((2), weight=2)
            hubframe.grid_columnconfigure((0,1,2), weight=1)
            
            # build frame for header
            headerframe = ctk.CTkFrame(hubframe, fg_color=WHITE) # fg_color=LIGHT_ORANGE)
            headerframe.grid_columnconfigure(0, weight=1)
            headerframe.grid_rowconfigure(0, weight=1)
            headerframe.grid(row=0, column=0, columnspan=3, sticky="nsew")

            header1 = ctk.CTkLabel(headerframe, text=" HOVEDMENU ", text_color=DARK_TEXT_COLOR, font=("Helvetica", 30, "bold"))
            header1.grid(row=0, column=0, padx=10, pady=(20, 10), sticky="nsew")

            # Build frames for buttons
            for idx, (name, func) in enumerate(menues.items()):
                #imagePath = self.resource_path(f"Images/0{idx+1}_Hub.png")
                imagePath = self.resource_path(f"../Images/0{idx+1}_Hub.png")

                frame = OpenSection(hubframe, func, button_text=name.upper(), imagePath=imagePath)
                frame.grid(row=1, column=idx, padx=10, pady=10, sticky="nsew")
                self.frames.append(frame)
            
            '''
            for idx, (name, func) in enumerate(menues.items()):
                    imagePath = f"C:/Projects/Fundora/Images/0{idx+1}_Hub.png" 
                    frame = OpenSection(hubframe, func, button_text=name.upper(), imagePath=imagePath)
                    frame.grid(row=1, column=idx, padx=10, pady=10,  sticky="nsew")

                    self.frames.append(frame)
            '''
        # make logout button
        self.lotout_button = ctk.CTkButton(hubframe, text="Log out", 
                                hover_color=LIGHT_PURPLE, 
                                fg_color=PURPLE, 
                                border_color=PURPLE, 
                                text_color=WHITE_TEXT_COLOR,
                                border_width=2,
                                command=logout_callback)
        
        self.lotout_button.grid(row=2, column=1, padx=10, pady=10, sticky="ew")
    

    def resource_path(self, rel_path: str) -> str:
        # Når app’en kører som PyInstaller onefile, pakkes assets ud i en temp-mappe (sys._MEIPASS)
        base = Path(getattr(sys, "_MEIPASS", Path(__file__).parent))
        return str(base / rel_path)


        # EXPORT/IMPORT DB BUTTONS
        '''
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
                    
        self.export_data_button.grid(row = 4, column=1, columnspan=1)
        
       
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
        '''

class OpenSection(ctk.CTkFrame): 
    def __init__(self, parent, menu_section, button_text = 'Section X', imagePath=""): 
        super().__init__(master = parent, fg_color=WHITE)
        #self.grid(column = 0, columnspan = 2, row = 0, sticky = 'nsew')
        self.menu_func = menu_section 

        # print (f"IMAGE PATH {imagePath}")
        pil_image = Image.open(imagePath)
        resizedImg = pil_image.resize((500, 480)) 
        butImg = CTkImage(light_image=resizedImg, dark_image=resizedImg, size=(500, 480))

        self.but1 = ctk.CTkButton(self, 
                                  text=button_text, 
                                  command       = self.menu_func, 
                                  compound      ="top", 
                                  text_color    = DARK_TEXT_COLOR,
                                  border_color  = DARK_ORANGE, 
                                  border_width  = 3,
                                  hover_color   = SUPERLIGHT_ORANGE, 
                                  corner_radius = 32, 
                                  fg_color      = 'transparent', 
                                  font          = ("Poppins", 20, "bold"),
                                  image=butImg) #Helvetica  hover_color="#006AC0", hover_color="#006AC0"
        self.but1.pack(expand=True, fill='both') # compound="top", image=butImg,
 

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



