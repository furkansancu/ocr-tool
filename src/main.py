import pathlib, os, filetype, requests, urllib
import tkinter, customtkinter, tkinterdnd2, pytesseract
from tkinter import filedialog, messagebox
from PIL import Image
from io import BytesIO

import components.util as util
import components.mem as mem

utils = util.Util()
memory = mem.MemoryHandler()

class OT_TK (customtkinter.CTk, tkinterdnd2.TkinterDnD.DnDWrapper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.TkdndVersion = tkinterdnd2.TkinterDnD._require(self)

customtkinter.set_appearance_mode("dark")

class NoTesseract:
    def __init__(self):
        self.window = OT_TK()
        self.window.geometry("376x366")
        self.window.iconbitmap("src/images/icon.ico")
        self.window.resizable(False, False)
        self.window.title("OCR Tool")
        self.window.configure(bg="white")
        self.TextFrame()
        self.ButtonsFrame()
        self.window.mainloop()

    def TextFrame(self):
        notesseract_text = open("src/texts/notesseract.txt", encoding="utf8").read()
        self.tPanelText = customtkinter.CTkCanvas(self.window, width=376, height=276, bg="#242424", highlightthickness=0, relief='ridge')
        self.tPanelText.create_text(
            188, 142,
            text=notesseract_text,
            fill="white",
            font="Helvetica 12 bold",
            justify="center",
            width=344
        )
        self.tPanelText.pack(side=tkinter.TOP, fill=tkinter.X)

    def ButtonsFrame(self):
        self.bFrame = customtkinter.CTkFrame(self.window, height=171, bg_color="#242424")
        self.bFrame.pack(side=tkinter.TOP, fill=tkinter.X, ipady=16, pady=24)
        self.bFrameDownload = customtkinter.CTkButton(self.bFrame, text="Download Tesseract OCR", cursor="hand2", command=lambda:utils.OpenLink("https://github.com/UB-Mannheim/tesseract/wiki"))
        self.bFrameDownload.pack(side=tkinter.LEFT, padx=16)
        self.bFrameLocate = customtkinter.CTkButton(self.bFrame, text="Locate Tesseract OCR", cursor="hand2", command=lambda:self.LocateTesseract())
        self.bFrameLocate.pack(side=tkinter.RIGHT, padx=16)
        
    def LocateTesseract(self):
        self.tesseractLocation = filedialog.askopenfilename(
            initialdir= pathlib.Path(os.environ["ProgramFiles"], "Tesseract-OCR\\tesseract.exe"),
            title= "Select tesseract.exe file",
            filetypes=(
                ("tesseract.exe", "tesseract.exe"),
                ("any file", "*.*")
            )
        )
        if (len(self.tesseractLocation) > 0):
            isTesseract = utils.TestTesseract(self.tesseractLocation)
            if not isTesseract:
                messagebox.showerror(
                    title="Tesseract could not identified.",
                    message="Selected file is not a tesseract-ocr file. Please select correct tesseract-ocr file."
                )
            else:
                pytesseract.pytesseract.tesseract_cmd = self.tesseractLocation
                self.Close()

    def Close(self):
        self.window.withdraw()
        OCRTool()

class OCRTool:
    def __init__ (self) :
        self.window = OT_TK()
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
        self.dndFrame = customtkinter.CTkFrame(self.window, width=360, height=180)
        self.dndFrame.pack_propagate(False)
        self.dndFrame.place(x=8, y=8)
        self.dndFrameButton = customtkinter.CTkButton(
            self.dndFrame,
            text="Drag and Drop Image or Select File",
            cursor="hand2",
            command=self.SelectImageFile
        )
        self.dndFrameButton.pack(fill=tkinter.BOTH, expand=True)
        self.dndFrameButton.drop_target_register(tkinterdnd2.DND_ALL)
        self.dndFrameButton.dnd_bind("<<Drop>>", self.DragAndDropImage)

    def ConsistencyArea(self):
        self.consistency = tkinter.IntVar(value=215)
        self.consFrame = customtkinter.CTkFrame(self.window, width=360, height=32)
        self.consFrame.place(x=8, y=196)
        self.consFrameTextFont = customtkinter.CTkFont(family="Ubuntu Medium", size=12, weight="bold")
        self.consFrameText = customtkinter.CTkLabel(self.consFrame, text="Consistency: ", font=self.consFrameTextFont)
        self.consFrameText.place(x=8, y=4)
        self.consFrameSlider = customtkinter.CTkSlider(self.consFrame, from_=50, to=235, variable=self.consistency, width=256)
        self.consFrameSlider.place(x=96, y=10)

    def OutputArea(self):
        self.optFrame = customtkinter.CTkFrame(self.window, width=360, height=372)
        self.optFrame.place(x=8, y=236)
        self.optFrame.pack_propagate(False)
        self.optText = customtkinter.CTkTextbox(self.optFrame)
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

        if len(self.imageFile) > 0:
            self.SetResult(self.imageFile)

    def DragAndDropImage(self, event):
        try:
            urllib.request.urlopen(event.data).getcode()
            isLink = True
        except:
            isLink = False
            
        if (isLink):
            response = requests.get(event.data)
            img = Image.open(BytesIO(response.content))
            self.SetResult(img)
        else:
            if (event.data[0] == "{" and event.data[-0] == "}"):
                event.data = event.data[1:-1]

            if filetype.is_image(event.data):
                self.SetResult(event.data)
            else:
                messagebox.showerror(
                    title="Selected file is not a image file.",
                    message="Selected file is not a image file. Please select a image file to run OCR."
                )
            
    def SetResult(self, image):
        image_file = Image.open(image)
        image_file = image_file.convert('L')
        image_file = image_file.point( lambda p: 255 if p > self.consistency.get() else 0 )
        image_file = image_file.convert('1')
        result = pytesseract.image_to_string(image=image_file)
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
        pytesseract.pytesseract.tesseract_cmd = memory_tesseract_path
        OCRTool()
    else:
        NoTesseract()