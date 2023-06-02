from util import TestTesseractPath;

print("This program requires Tesseract OCR to run if you have not installed")
print("please install via this link: https://tesseract-ocr.github.io/tessdoc/Installation.html")
tesseractPath = False

while (tesseractPath == False):
    tesseractPath = input("Please enter Tesseract OCR location: ") or "C:\Program Files\Tesseract-OCR"
    tesseractPath = TestTesseractPath(tesseractPath)

    if (tesseractPath == False):
        print("Tesseract not found")

print("Tesseract succesfully found.")