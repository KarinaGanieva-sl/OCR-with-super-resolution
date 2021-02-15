from PIL import Image
import pytesseract
import cv2
import os


# show the output images
# cv2.imshow("Image", image)
#cv2.imshow("Output", gray)
#cv2.waitKey(0)

def preprocess(image, thresh=True, blur=False):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    if thresh:
        gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    if blur:
        gray = cv2.medianBlur(gray, 3)
    return gray


def process_ocr(gray):
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    # write the grayscale image to disk as a temporary file so we can
    # apply OCR to it
    filename = "{}.png".format(os.getpid())
    cv2.imwrite(filename, gray)
    text = pytesseract.image_to_string(Image.open(filename))
    os.remove(filename)
    return text
