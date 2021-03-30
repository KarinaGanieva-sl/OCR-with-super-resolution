from pdf2image import convert_from_path, convert_from_bytes
from pdf2image.exceptions import (
    PDFInfoNotInstalledError,
    PDFPageCountError,
    PDFSyntaxError
)
from os import listdir
from os.path import isfile, join


def convert_pdf_to_jpeg(folder_name):
    images_folder_name = 'images/'
    files = [f for f in listdir(folder_name) if isfile(join(folder_name, f))]
    for file in files:
        print(file)
        images = convert_from_path(folder_name+'/'+file, poppler_path=r"C:\Program Files\Release-21.03.0\poppler-21.03.0\Library\bin")
        i = 0
        for im in images:
            im.save(images_folder_name + str(i) + '.jpg')
            i += 1
    return images_folder_name
