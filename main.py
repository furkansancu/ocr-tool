from pathlib import Path

from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
from tkinterdnd2 import DND_FILES, TkinterDnD
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\\tesseract.exe"

# print("This program requires Tesseract OCR to run if you have not installed")
# print("please install via this link: https://tesseract-ocr.github.io/tessdoc/Installation.html")
# tesseractPath = False

# while (tesseractPath == False):
#     tesseractPath = input("Please enter Tesseract OCR location: ") or "C:\Program Files\Tesseract-OCR"
#     tesseractPath = TestTesseractPath(tesseractPath)

#     if (tesseractPath == False):
#         print("Tesseract not found")
# print("Tesseract succesfully found.")

class OCRTOOL:
    def __init__(self, root):
        self.window = root
        self.SetOnTop()
        self.SetOnCenter()
        self.dndIm = Image.open("pictures/dnd.png")
        self.dndImg = ImageTk.PhotoImage(self.dndIm)
        self.lb = Label(self.window, image=self.dndImg, width= 301, cursor="hand2", background="#dce4e2")
        self.lb.drop_target_register(DND_FILES)
        self.lb.dnd_bind('<<Drop>>', lambda e: self.UpdateFilePath(e.data))
        self.lb.bind("<Button-1>", lambda e: self.SetFilePath())
        self.lb.pack(side= TOP, ipady=16, ipadx=0)
        self.result = Text(self.window, height=14, width=40)
        self.result.pack(side= TOP)
        
    def SetOnTop(self):
        self.window.attributes('-topmost', True)
        self.window.update()
        self.window.attributes('-topmost', False)

    def SetOnCenter(self):
        w = self.window.winfo_width()
        h = self.window.winfo_height()
        ws = self.window.winfo_screenwidth()
        hs = self.window.winfo_screenheight()
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)
        self.window.geometry('+%d+%d'%(x, y))

    def SetOCRPath():
        pass

    def SetFilePath(self):
        self.window.filepath = filedialog.askopenfilename(
            initialdir= Path.home() / "Downloads",
            title = "Select Image",
            filetypes=(
                ("image files", ("*.jpg", "*.jpeg", "*.png")),
                ("jpeg files", ("*.jpg", "*.jpeg")),
                ("png files", "*.png"),
                ("all files", "*.*")
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
        image_file = image_file.point( lambda p: 255 if p > 100 else 0 )
        text = pytesseract.image_to_string(image_file)
        self.result.delete("1.0", "end")
        self.result.insert(END, text)

if __name__ == '__main__':
    window = TkinterDnD.Tk()
    window.title("OCR Tool")
    window.iconbitmap("pictures/favicon.ico")
    window.geometry("333x444")
    window['background'] = "#dce4e2"
    window.resizable(False, False)
    OCRTOOL(window)
    window.mainloop()