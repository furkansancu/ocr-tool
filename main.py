from pathlib import Path
from os import environ, getenv, path, makedirs
import sys

from tkinter import *
from tkinter import filedialog
from tkinter import font as tkFont
from tkinter import messagebox
from PIL import Image, ImageTk
from tkinterdnd2 import DND_FILES, TkinterDnD
import pytesseract
import pickle
import webbrowser

from util import TestTesseractPath

settings_dir = Path(getenv("APPDATA"), "OCR-TOOL-furkansancu")
if not path.exists(settings_dir): makedirs(settings_dir)
settings_filepath = settings_dir.joinpath("save.p")

try: stored_data = pickle.load( open( settings_filepath, "rb" ) )
except:
    stored_data = {"tesseract_path": None}
    f = open(settings_filepath, 'a+')
    f.close()
    pickle.dump({"tesseract_path": stored_data["tesseract_path"]}, open( settings_filepath, "wb" ))

def callback(url):
    webbrowser.open_new(url)

def checkTesseractPath(path):
    if (path == None): return False
    else:
        if (TestTesseractPath(path) != False):
            setTesseractPath(path)
            return True
        else:
            return False

def setTesseractPath(path):
    pytesseract.pytesseract.tesseract_cmd = r"" + path

tesseract_found = checkTesseractPath(stored_data["tesseract_path"])

def resourcePath(relative_path):
    base_path = getattr(sys, '_MEIPASS', path.dirname(path.abspath(__file__)))
    return path.join(base_path, relative_path)

class OCRTOOL:
    def __init__(self, root):
        self.window = root
        if (tesseract_found == False): self.SetOCRWindow()
        self.consistency = IntVar(value=100)
        self.SetOnTop( self.window )
        self.SetOnCenter( self.window )
        self.dndImg = ImageTk.PhotoImage(file=resourcePath("pictures/dnd.png"))
        self.lb = Label(self.window, image=self.dndImg, width= 301, cursor="hand2", background="#dce4e2")
        self.lb.drop_target_register(DND_FILES)
        self.lb.dnd_bind('<<Drop>>', lambda e: self.UpdateFilePath(e.data))
        self.lb.bind("<Button-1>", lambda e: self.SetFilePath())
        self.lb.pack(side= TOP, ipady=16, ipadx=0)
        self.cn = Scale(self.window, from_=20, to=235, orient= HORIZONTAL, width=10, length=301, variable=self.consistency)
        self.cn.pack(side= TOP, expand= True, pady=6)
        self.result = Text(self.window, height=14, width=40)
        self.result.pack(side= TOP, expand=TRUE)
            
    def SetOnTop(self, window):
        window.attributes('-topmost', True)
        window.update()
        window.attributes('-topmost', False)

    def SetOnCenter(self, window):
        w = window.winfo_width()
        h = window.winfo_height()
        ws = window.winfo_screenwidth()
        hs = window.winfo_screenheight()
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)
        window.geometry('+%d+%d'%(x, y))

    def SetOCRWindow(self):
        self.window.withdraw()
        self.top= Toplevel(self.window)
        self.top.protocol("WM_DELETE_WINDOW", self.TopLevelClosed)
        self.top.geometry("444x275")
        self.top.title("OCR Tool")
        self.top['background'] = "#dce4e2"
        self.top.resizable(False, False)
        self.top.lbl0 = Label(self.top, text="", background="#dce4e2").pack(side=TOP, pady=8)
        self.top.lbl1 = Label(self.top, text="This program uses Tesseract OCR and to use that program").pack(side= TOP)
        self.top.lbl2 = Label(self.top, text="It is essentail to have Tesseract OCR installed on your computer.").pack(side= TOP)
        self.top.lbl3 = Label(self.top, text="If you have not installed it, please do it via this link:").pack(side= TOP)
        self.top.lbl4 = Label(self.top, text="https://github.com/UB-Mannheim/tesseract/wiki", foreground="#0000FF", cursor="hand2")
        self.top.lbl4.bind("<Button-1>", lambda e: callback("https://github.com/UB-Mannheim/tesseract/wiki"))
        self.top.lbl4.pack(side= TOP, pady=8)
        self.top.lbl5 = Label(self.top, text="If you already have Tesseract OCR installed on your computer,").pack(side= TOP)
        self.top.lbl6 = Label(self.top, text="Please locate it:").pack(side= TOP)
        helv = tkFont.Font(family='Helvetica', size=8, weight='bold')
        self.top.btn = Button(self.top, text="Locate Tesseract OCR", font=helv, cursor="hand2", command=self.SetOCRPath).pack(side= TOP, pady=16, padx=32, ipadx=8, ipady=4)
        self.SetOnCenter(self.top)
        self.SetOnTop(self.top)

    def TopLevelClosed (self):
        exit(1)

    def SetOCRPath (self):
        global tesseract_found
        stored_data["tesseract_path"] = filedialog.askopenfilename(
            initialdir= environ['PROGRAMFILES']+"\\Tesseract-OCR",
            title = "Select tesseract.exe",
            filetypes=(
                ("tesseract.exe", "tesseract.exe"),
                ("any file", "*.*")
            )
        )
        if(stored_data["tesseract_path"] != ""):
            tesseract_found = checkTesseractPath(stored_data["tesseract_path"])
            if (tesseract_found == False):
                messagebox.showerror(title="Wrong file", message="Selected file is not running correctly.")
            else:
                pickle.dump({"tesseract_path": stored_data["tesseract_path"]}, open( settings_filepath, "wb" ))
                self.window.deiconify()
                self.top.withdraw()

    def SetFilePath(self):
        self.window.filepath = filedialog.askopenfilename(
            initialdir= Path.home() / "Downloads",
            title = "Select Image",
            filetypes=(
                ("image files", ("*.jpg", "*.jpeg", "*.png")),
                ("jpeg files", ("*.jpg", "*.jpeg")),
                ("png files", "*.png")
            )
        )
        self.FilePathUpdated()

    def UpdateFilePath (self, path):
        self.window.filepath = path[1:-1]
        self.FilePathUpdated()

    def FilePathUpdated (self):
        if (self.window.filepath != None):
            self.ScanImage()
            
    def ScanImage (self):
        image_file = Image.open(self.window.filepath)
        image_file = image_file.point( lambda p: 255 if p > self.consistency.get() else 0 )
        text = pytesseract.image_to_string(image_file)
        self.result.delete("1.0", "end")
        self.result.insert(END, text)

if __name__ == '__main__':
    window = TkinterDnD.Tk()
    window.title("OCR Tool")
    window.geometry("333x555")
    window['background'] = "#dce4e2"
    window.resizable(False, False)
    OCRTOOL(window)
    window.mainloop()