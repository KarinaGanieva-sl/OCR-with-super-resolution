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
    for image in images_folders:
        print(image)
        image_read = cv2.imread(image_folder_name + '/' + image)
        image_hr = esrgan.to_HR(image_read)
        images_hr.append(image_hr)
    return images_hr


def read_images(image_folder):
    images = []
    images_folders = [f for f in listdir(image_folder) if isfile(join(image_folder, f))]
    for image in images_folders:
        print(image)
        image_read = cv2.imread(image_folder + '/' + image)
        images.append(image_read)
    return images


def preprocess(images):
    grays = []
    for image in images:
        gray = ocr.preprocess(image, thresh=True, blur=False)
        grays.append(gray)
    return grays


def process_ocr(grays):
    output = []
    for gray in grays:
        output.append(ocr.process_ocr(gray))
    return output


def compute_levenshtein(parsed_pdf, output):
    results = []
    for i in range(len(parsed_pdf)):
        results.append(distance(parsed_pdf[i], output[i]))
    return results


ap = argparse.ArgumentParser()
ap.add_argument("-f", "--pdf folder", required=True, default='art', help="low resolution images")
ap.add_argument("-m", "--model", required=True, default='esrgan', help="super resolution model")
ap.add_argument("-p", "--preprocess", type=str, default="thresh", help="type of preprocessing to be done")
args = vars(ap.parse_args())


image_folder = pdf_to_image.convert_pdf_to_jpeg(args['pdf folder'])
parsed_pdf = pdf_to_text.parse_pdf(args['pdf folder'])
grays = preprocess(read_images(image_folder))
output = process_ocr(grays)
results = compute_levenshtein(parsed_pdf, output)
print(results)
'''images_hr = images_to_HR(image_folder)
grays = preprocess(images_hr)
output = process_ocr(grays)
results = compute_levenshtein(parsed_pdf, output)
print(results)'''
