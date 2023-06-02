from subprocess import run

def TestTesseractPath (path):
    withexe = run(f'"{path}" --version',capture_output=True,shell=True)
    if (withexe.stderr):
        withoutexe = run(f'"{path}"\\tesseract.exe --version',capture_output=True,shell=True)
        if (withoutexe.stderr): return False
        else: return path + "\\tesseract.exe"
    else: return True
