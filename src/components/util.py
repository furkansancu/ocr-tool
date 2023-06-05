import os, pathlib
import subprocess
import webbrowser

default_tesseract_paths = [
    pathlib.Path(os.environ["ProgramFiles"], "Tesseract-OCR\\tesseract.exe"),
    pathlib.Path(os.environ["LOCALAPPDATA"], "Tesseract-OCR\\tesseract.exe")
]

class Util:
    def __init__(self):
        pass
    
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