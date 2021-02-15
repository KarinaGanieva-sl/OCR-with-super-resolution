import argparse
import cv2
import ocr
import esrgan

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, default='LR/1.png', help="low resolution image")
ap.add_argument("-m", "--model", required=True, default='esrgan', help="super resolution model")
ap.add_argument("-p", "--preprocess", type=str, default="thresh", help="type of preprocessing to be done")
args = vars(ap.parse_args())


image = cv2.imread(args["image"])
image_hr = esrgan.to_HR(image)
gray = ocr.preprocess(image, args["preprocess"] == 'thresh', args["preprocess"] == "blur")
output = ocr.process_ocr(gray)
print(output)
