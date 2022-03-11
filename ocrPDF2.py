from pdf2image import convert_from_path
import os
import time
from PyPDF2 import PdfFileMerger
import shutil
import pytesseract
from tkinter import Tk
from tkinter.filedialog import askdirectory# , askopenfilename
import threading

try:
    from PIL import Image
except ImportError:
    import Image

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
    pdfName = (fileSelection.split("/"))[-1]
    # print(pdfName)

    outfile1 = (fileSelection.split("/"))[: len(fileSelection.split("/")) - 1]
    FinalLocation = ""
    for i in outfile1:
        FinalLocation += i + "/"
    outputDirectory = pdfName + "temp/"

    return outputDirectory, fileSelection, FinalLocation, pdfName


def convert2png(file, outputDir):
    if not os.path.exists(outputDir):
        os.makedirs(outputDir)

    pages = convert_from_path(file, 150)
    counter = 1
    for page in pages:
        myfile = outputDir + 'output' + str(counter) + '.png'
        counter = counter + 1
        page.save(myfile, "PNG")
        # print(myfile)


def convert2pdf(outputDir):
    pageNum = 1

    for filename in os.listdir(outputDir):
        pdf = pytesseract.image_to_pdf_or_hocr(outputDir + '/' + filename, extension='pdf')
        with open(outputDir + '/' + str(pageNum) + '.pdf', 'w+b') as f:
            f.write(pdf)  # pdf type is bytes by default
        pageNum += 1


def mergePDFs(outputDir, outfile, pdfFile):
    merge_list = []
    if not os.path.exists(outfile + "/converted"):
        os.makedirs(outfile + "/converted")

    for x in os.listdir(outputDir):
        if not x.endswith('.pdf'):
            continue
        merge_list.append(outputDir + x)

    merger = PdfFileMerger()

    for pdf in merge_list:
        merger.append(pdf)

    merger.write(outfile + "/converted/" + pdfFile[: -4] + 'OCR.pdf')  # your output directory
    print(outfile + "/converted/")

    merger.close()


def conversion(fileAddress):
    #print(Selection + "/" + file_pdf)
    outputDir, filename, outfile, pdfFile = fileSelect(fileAddress)
    convert2png(filename, outputDir)
    convert2pdf(outputDir)
    mergePDFs(outputDir, outfile, pdfFile)
    # shutil.rmtree(outputDir)


Tk().withdraw()
Selection = askdirectory() # Select Directory of PDFs
if Selection == "":
    print("No Directory Selected")
    quit()

threads = []

for file_pdf in os.listdir(Selection):
    if ".pdf" in file_pdf:
        fileAddress = (Selection + "/" + file_pdf)
        x = threading.Thread(target=conversion, args=[fileAddress])
        x.start()
        threads.append(x)
    else:
        print("Skipping", file_pdf)

for thread in threads:
    thread.join()
print(time.time() - start)
