import os, sys, pathlib
import subprocess
import webbrowser

default_tesseract_paths = [
    pathlib.Path(os.environ["ProgramFiles"], "Tesseract-OCR\\tesseract.exe"),
    pathlib.Path(os.environ["LOCALAPPDATA"], "Tesseract-OCR\\tesseract.exe")
]

class Util:
    def TestTesseract(self, path):
        try:
            process = subprocess.Popen(f'"{path}" --version', stdout=subprocess.PIPE)
            stdout = str(process.communicate())
            return stdout[0:14] == "(b'tesseract v"
        except:
            return False
    
    def SearchTesseract(self, memory):
        for path in default_tesseract_paths:
            found_tesseract = self.TestTesseract(path)
            if (found_tesseract):
                memory.SetData("tesseract_path", path)
                return True
        return False
    
    def OpenLink(self, link):
        webbrowser.open(link)
        
    def GetNoTesseractText(self):
        return "This program uses Tesseract OCR for character recognition.\nHaving Tesseract OCR installed on your computer is vital to run this program.\nIf you have not installed please click “Download Tesseract OCR” button.\nIf you already had installed it, please locate it via clicking the “Locate Tesseract OCR” button."