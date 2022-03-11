from pdf2image import convert_from_path
import os
import time
from PyPDF2 import PdfFileMerger
import shutil
import pytesseract
from tkinter import Tk
from tkinter.filedialog import askdirectory  # , askopenfilename
import threading
from PIL import Image

start = time.time()


def fileSelect(fileSelection):
    if fileSelection == "":
        print("No File Selected")
        quit()
    if ".pdf" in fileSelection:
        pass
    else:
        print("Invalid File")
        quit()

    fileSelection = str(fileSelection)
    pdfName = (fileSelection.split("/"))[-1]  # Saves name of file with ".pdf"

    outputDirectory = pdfName + "temp/"  # Temporary Output Directory to store Images

    return outputDirectory, fileSelection, pdfName


def convert2png(file, outputDir):
    if not os.path.exists(outputDir):
        os.makedirs(outputDir)

    pages = convert_from_path(file, 150)
    counter = '1'
    for page in pages:
        myfile = outputDir + 'output' + counter + '.png'
        counter += '1'
        page.save(myfile, "PNG")


def compress(outputDir):
    for filename in os.listdir(outputDir):
        img = Image.open(outputDir + '/' + filename)
        img = img.convert('L')
        img.save(outputDir + filename, optimize=True, quality=100)


def convert2pdf(outputDir):
    pageNum = '1'

    for filename in os.listdir(outputDir):
        pdf = pytesseract.image_to_pdf_or_hocr(outputDir + '/' + filename, extension='pdf')
        with open(outputDir + '/' + filename + '.pdf', 'w+b') as f:
            f.write(pdf)  # pdf type is bytes by default
        pageNum += '1'


def mergePDFs(outputDir, outfile, pdfFile):
    merge_list = []
    if not os.path.exists(outfile + "/converted1"):
        os.makedirs(outfile + "/converted1")

    for name in os.listdir(outputDir):
        if not name.endswith('.pdf'):
            continue
        merge_list.append(outputDir + x)
    merge_list.sort()

    merger = PdfFileMerger()

    for pdf in merge_list:
        merger.append(pdf)

    merger.write(outfile + "/converted1/" + pdfFile[: -4] + 'OCR.pdf')  # Final Output Directory
    merger.close()


def conversion(FileAddress, DirAddress):
    print(threading.current_thread().name)

    outputDir, filename, pdfFile = fileSelect(FileAddress)
    convert2png(filename, outputDir)
    compress(outputDir)
    convert2pdf(outputDir)
    mergePDFs(outputDir, DirAddress, pdfFile)
    shutil.rmtree(outputDir)

 
Tk().withdraw()
Selection = askdirectory()  # Select Directory of PDFs

if Selection == "":
    print("No Directory Selected")
    quit()

threads = []

# for file_pdf in os.listdir(Selection):
#     if ".pdf" in file_pdf:
#         fileAddress = (Selection + "/" + file_pdf)
#         conversion(fileAddress, Selection)

for file_pdf in os.listdir(Selection):

    if ".pdf" in file_pdf and "temp" not in file_pdf:
        time.sleep(0.5)
        fileAddress = (Selection + "/" + file_pdf)
        x = threading.Thread(target=conversion, args=[fileAddress, Selection])
        x.start()
        threads.append(x)
    else:
        print("Skipping", file_pdf)

for thread in threads:
    thread.join()

print(time.time() - start)
