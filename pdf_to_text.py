import os
import tempfile
from pdf2image import convert_from_path
from PIL import Image
import pytesseract
import sys, getopt
import datetime


def store_text_file(saveText, pgindx, pdfindx, pdfName):
    tempName = pdfName[8:]
    fName = tempName[:-4]
    if (str(os.path.exists('./outputs/' + fName))== "False" ):
        os.mkdir("./outputs/" + fName)
    f = open("./outputs/" + fName + "/" + "page" + pgindx + ".txt", "w")
    f.write(saveText)
    f.close()


def convert_to_text(img, pgindx, pdfindex, pdfName):
    text = pytesseract.image_to_string(img)
    store_text_file(text,pgindx, pdfindex, pdfName)


def extract_image_fromPdf(fileName, pdfindx):
    with tempfile.TemporaryDirectory() as path:
        images_from_path = convert_from_path(fileName, output_folder=path)
        pages = range(images_from_path.__len__())
        base_filename = os.path.splitext(os.path.basename(fileName))[0]

        for pgindx in pages:
          # call convert to text
            convert_to_text(images_from_path[pgindx],str(pgindx + 1), str(pdfindx), fileName)



def start_process(fname, pdfindx):
    old_time = datetime.datetime.now()
    extract_image_fromPdf(fname, pdfindx)
    new_time = datetime.datetime.now()
    print('Duration >>> ' + str((new_time - old_time).total_seconds()) + ' seconds')


def main(argv):
    # init outputs
    old_time = datetime.datetime.now()
    for root, dirs, files in os.walk(str(argv[0])):
        pdfindx = 1
        for filename in files:
            print(filename)
            start_process("./inputs/"+filename, pdfindx )
            pdfindx += 1
        else:
            new_time = datetime.datetime.now()
            print('Total Duration >>> ' + str(new_time - old_time))



if __name__ == "__main__":
   main(sys.argv[1:])
