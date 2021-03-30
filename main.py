import argparse
import cv2
from Levenshtein import *
import ocr
import esrgan
import pdf_to_image
import pdf_to_text
from os import listdir
from os.path import isfile, join


def images_to_HR(image_folder_name):
    images_hr = []
    images_folders = [f for f in listdir(image_folder_name) if isfile(join(image_folder_name, f))]
    for image in listdir(images_folders):
        d = {'file': image}
        image_read = cv2.imread(image)
        d['image'] = esrgan.to_HR(image_read)
        images_hr.append(d)
    return images_hr


def preprocess(images):
    grays = []
    for image in images:
        d = {'file': image['file'], 'image': ocr.preprocess(image, thresh=True, blur=False)}
        grays.append(d)
    return grays


def process_ocr(grays):
    output = []
    for gray in grays:
        d = {'file': grays['file'], 'image': ocr.process_ocr()}
        output.append(ocr.preprocess(gray, thresh=True, blur=False))
    return grays


def compute_levenshtein(parsed_pdf, output):
    results = []
    for i in range(parsed_pdf):
        results.append(distance(parsed_pdf[i], output[i]))
    return results


ap = argparse.ArgumentParser()
ap.add_argument("-f", "--pdf folder", required=True, default='LR/1.png', help="low resolution image")
ap.add_argument("-m", "--model", required=True, default='esrgan', help="super resolution model")
ap.add_argument("-p", "--preprocess", type=str, default="thresh", help="type of preprocessing to be done")
args = vars(ap.parse_args())


image_folder = pdf_to_image.convert_pdf_to_jpeg(args['pdf folder'])
images_hr = images_to_HR(image_folder)
grays = preprocess(images_hr)
output = process_ocr(grays)
parsed_pdf = pdf_to_text.parse_pdf(args['pdf folder'])
results = compute_levenshtein(parsed_pdf, output)
print(results)
