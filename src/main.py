import pathlib, os
import tkinter, ttkthemes, pytesseract
from tkinter import filedialog, messagebox, ttk, font
from PIL import Image, ImageTk

import components.util as util
import components.mem as mem

utils = util.Util()
memory = mem.MemoryHandler()

def SetTesseractPath(path):
    pytesseract.pytesseract.tesseract_cmd = path

class NoTesseract:
    def __init__(self):
        self.window = ttkthemes.ThemedTk(theme="arc")
        self.window.geometry("376x512")
        self.window.iconbitmap("src/images/icon.ico")
        self.window.resizable(False, False)
        self.window.title("OCR Tool")
        self.window.configure(bg="white")
        self.TextFrame()
        self.ButtonsFrame()
        self.window.mainloop()

    def TextFrame(self):
        self.tPanel = tkinter.Frame(self.window, height=341)
        self.tPanel.pack(expand=True, side=tkinter.TOP)
        self.tPanelImage = ImageTk.PhotoImage(Image.open("src/images/notesseract.jpg"))
        self.tPanelLabel = ttk.Label(self.window, image=self.tPanelImage)
        self.tPanelLabel.place(x=0, y=0)

    def ButtonsFrame(self):
        self.bFrame = tkinter.Frame(self.window, height=171)
        self.bFrame.configure(bg="white")
        self.bFrame.pack(side=tkinter.TOP, ipadx=12, ipady=64)
        self.bFrameDownload = ttk.Button(self.bFrame, text="Download Tesseract OCR", cursor="hand2", command=lambda:utils.OpenLink("https://github.com/UB-Mannheim/tesseract/wiki"))
        self.bFrameDownload.pack(side=tkinter.LEFT)
        self.bFrameLocate = ttk.Button(self.bFrame, text="Locate Tesseract OCR", cursor="hand2", command=lambda:self.LocateTesseract())
        self.bFrameLocate.pack(side=tkinter.RIGHT)
        
    def LocateTesseract(self):
        self.tesseractLocation = filedialog.askopenfilename(
            initialdir= util.default_tesseract_paths,
            title= "Select tesseract.exe file",
            filetypes=(
                ("tesseract.exe", "tesseract.exe"),
                ("any file", "*.*")
            )
        )
        if (self.tesseractLocation != None):
            isTesseract = utils.TestTesseract(self.tesseractLocation)
            if not isTesseract:
                messagebox.showerror(
                    title="Tesseract could not identified.",
                    message="Selected file is not a tesseract-ocr file. Please select correct tesseract-ocr file."
                )
            else:
                SetTesseractPath(self.tesseractLocation)
                self.Close()

    def Close(self):
        OCRTool()
        self.window.withdraw()

class OCRTool:
    def __init__ (self) :
        self.window = ttkthemes.ThemedTk(theme="arc")
        self.window.geometry("376x616")
        self.window.iconbitmap("src/images/icon.ico")
        self.window.resizable(False, False)
        self.window.title("OCR Tool")
        self.window.configure(bg="white")
        self.DnDArea()
        self.ConsistencyArea()
        self.OutputArea()
        self.window.mainloop()

    def DnDArea(self):
        self.dndFrame = tkinter.Frame(self.window, width=360, height=180)
        self.dndFrame.configure(bg="#fff")
        self.dndFrame.pack_propagate(False)
        self.dndFrame.place(x=8, y=8)
        self.dndFrameButton = ttk.Button(
            self.dndFrame,
            text="Drag and Drop Image or Select File",
            cursor="hand2",
            command=self.SelectImageFile
        )
        self.dndFrameButton.pack(fill=tkinter.BOTH, expand=True)

    def ConsistencyArea(self):
        self.consistency = tkinter.IntVar(value=180)
        self.consFrame = tkinter.Frame(self.window, width=360, height=32)
        self.consFrame.configure(bg="white")
        self.consFrame.place(x=8, y=196)
        self.consFrameTextFont = font.Font(family="Ubuntu Medium", size=10, weight="bold")
        self.consFrameText = ttk.Label(self.consFrame, text="Consistency: ", font=self.consFrameTextFont, background="white")
        self.consFrameText.place(x=8, y=8)
        self.consFrameSlider = ttk.Scale(self.consFrame, from_=40, to=255, length=256, variable=self.consistency)
        self.consFrameSlider.place(x=96, y=10)

    def OutputArea(self):
        self.optFrame = tkinter.Frame(self.window, width=360, height=372)
        self.optFrame.place(x=8, y=236)
        self.optFrame.pack_propagate(False)
        self.optText = tkinter.Text(self.optFrame)
        self.optText.pack(fill=tkinter.BOTH, expand=True, ipadx=8, ipady=8)

    def SelectImageFile(self):
        self.imageFile = filedialog.askopenfilename(
            initialdir= os.path.join(pathlib.Path.home(), "Downloads"),
            title= "Select tesseract.exe file",
            filetypes=(
                ("Image files", ("*.jpg", "*.jpeg", ".png")),
                ("any file", "*.*")
            )
        )

        if self.imageFile != None:
            self.SetResult(self.imageFile)
            
    def SetResult(self, image):
        result = pytesseract.image_to_string(image=image)
        self.optText.delete("1.0", "end")
        self.optText.insert(tkinter.END, result)

if __name__ == '__main__':
    memory_tesseract_path = memory.GetData("tesseract_path")
    if not memory_tesseract_path == None: tesseract_located = utils.TestTesseract(memory_tesseract_path)
    else: tesseract_located = False
    if not tesseract_located:
        tesseract_located = utils.SearchTesseract(memory)
        memory_tesseract_path = memory.GetData("tesseract_path")

    if tesseract_located:
        SetTesseractPath(memory_tesseract_path)
        OCRTool()
    else:
        NoTesseract()

# def resourcePath(relative_path):
#     base_path = getattr(sys, '_MEIPASS', path.dirname(path.abspath(__file__)))
#     return path.join(base_path, relative_path)

# class OCRTOOL:
#     def __init__(self, root):
#         self.window = root
#         if (tesseract_found == False): self.SetOCRWindow()
#         self.consistency = IntVar(value=100)
#         self.SetOnTop( self.window )
#         self.SetOnCenter( self.window )
#         # self.dndImg = ImageTk.PhotoImage(file=resourcePath("pictures/dnd.png"))
#         # self.lb = Label(self.window, image=self.dndImg, width= 301, cursor="hand2", background="#dce4e2")
#         # self.lb.drop_target_register(DND_FILES)
#         # self.lb.dnd_bind('<<Drop>>', lambda e: self.UpdateFilePath(e.data))
#         # self.lb.bind("<Button-1>", lambda e: self.SetFilePath())
#         # self.lb.pack(side= TOP, ipady=16, ipadx=0)
#         self.cn = ttk.Scale(self.window, from_=20, to=235, orient= HORIZONTAL, length=301, variable=self.consistency)
#         self.cn.pack(side= TOP, expand= True, pady=6)
#         self.result = Text(self.window, height=14, width=40)
#         self.result.pack(side= TOP, expand=TRUE)
            
#     def SetOnTop(self, window):
#         window.attributes('-topmost', True)
#         window.update()
#         window.attributes('-topmost', False)

#     def SetOnCenter(self, window):
#         w = window.winfo_width()
#         h = window.winfo_height()
#         ws = window.winfo_screenwidth()
#         hs = window.winfo_screenheight()
#         x = (ws/2) - (w/2)
#         y = (hs/2) - (h/2)
#         window.geometry('+%d+%d'%(x, y))

#     def SetOCRWindow(self):
#         self.window.withdraw()
#         self.top= Toplevel(self.window)
#         self.top.protocol("WM_DELETE_WINDOW", self.TopLevelClosed)
#         self.top.geometry("444x275")
#         self.top.title("OCR Tool")
#         self.top['background'] = "#dce4e2"
#         self.top.resizable(False, False)
#         self.top.lbl0 = Label(self.top, text="", background="#dce4e2").pack(side=TOP, pady=8)
#         self.top.lbl1 = Label(self.top, text="This program uses Tesseract OCR and to use that program").pack(side= TOP)
#         self.top.lbl2 = Label(self.top, text="It is essentail to have Tesseract OCR installed on your computer.").pack(side= TOP)
#         self.top.lbl3 = Label(self.top, text="If you have not installed it, please do it via this link:").pack(side= TOP)
#         self.top.lbl4 = Label(self.top, text="https://github.com/UB-Mannheim/tesseract/wiki", foreground="#0000FF", cursor="hand2")
#         self.top.lbl4.bind("<Button-1>", lambda e: callback("https://github.com/UB-Mannheim/tesseract/wiki"))
#         self.top.lbl4.pack(side= TOP, pady=8)
#         self.top.lbl5 = Label(self.top, text="If you already have Tesseract OCR installed on your computer,").pack(side= TOP)
#         self.top.lbl6 = Label(self.top, text="Please locate it:").pack(side= TOP)
#         helv = tkFont.Font(family='Helvetica', size=8, weight='bold')
#         self.top.btn = Button(self.top, text="Locate Tesseract OCR", font=helv, cursor="hand2", command=self.SetOCRPath).pack(side= TOP, pady=16, padx=32, ipadx=8, ipady=4)
#         self.SetOnCenter(self.top)
#         self.SetOnTop(self.top)

#     def TopLevelClosed (self):
#         exit(1)

#     def SetOCRPath (self):
#         global tesseract_found
#         stored_data["tesseract_path"] = filedialog.askopenfilename(
#             initialdir= environ['PROGRAMFILES']+"\\Tesseract-OCR",
#             title = "Select tesseract.exe",
#             filetypes=(
#                 ("tesseract.exe", "tesseract.exe"),
#                 ("any file", "*.*")
#             )
#         )
#         if(stored_data["tesseract_path"] != ""):
#             tesseract_found = checkTesseractPath(stored_data["tesseract_path"])
#             if (tesseract_found == False):
#                 messagebox.showerror(title="Wrong file", message="Selected file is not running correctly.")
#             else:
#                 pickle.dump({"tesseract_path": stored_data["tesseract_path"]}, open( settings_filepath, "wb" ))
#                 self.window.deiconify()
#                 self.top.withdraw()

#     def SetFilePath(self):
#         self.window.filepath = filedialog.askopenfilename(
#             initialdir= Path.home() / "Downloads",
#             title = "Select Image",
#             filetypes=(
#                 ("image files", ("*.jpg", "*.jpeg", "*.png")),
#                 ("jpeg files", ("*.jpg", "*.jpeg")),
#                 ("png files", "*.png")
#             )
#         )
#         self.FilePathUpdated()

#     def UpdateFilePath (self, path):
#         self.window.filepath = path[1:-1]
#         self.FilePathUpdated()

#     def FilePathUpdated (self):
#         if (self.window.filepath != None):
#             self.ScanImage()
            
#     def ScanImage (self):
#         image_file = Image.open(self.window.filepath)
#         image_file = image_file.point( lambda p: 255 if p > self.consistency.get() else 0 )
#         text = pytesseract.image_to_string(image_file)
#         self.result.delete("1.0", "end")
#         self.result.insert(END, text)