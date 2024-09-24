# from PIL import Image
import cv2 
# from .methods import *
import pytesseract as py
import os
from skimage.filters import threshold_sauvola
import numpy as np
def run_ocr(image_Name):
    img_folder = "media/"
    img_path = os.path.join(img_folder, image_Name)
    img = cv2.imread(img_path)
    print(img_path)
    # #Image processing
    # img_bw = img_Processing(img)
    
    # #Edge Detection
    # edged=cv2.Canny(img_bw,10,50)

    # #Contures detection and Prespective transformation
    # image_output  = contures_detection(edged,img)
    
    # #OCR section 
    # ocr_img = img_Processing(img)
    # config = "--oem 3 --psm 6"
    # ocr_text=py.image_to_string(ocr_img, config=config, lang='eng')
    
    # #testing
    # # cv2.imshow("test",f.rescaleFrame(img_bw))
    # # cv2.waitKey(0)
    # save_folder = "processed_img/"
    # img_path=os.path.join(save_folder, image_Name)
    # cv2.imwrite(img_path,ocr_img)
    # # data={
    # #     'ocr':ocr_text,
    # #     'NA':'test'
    # # }
    # return ocr_text

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Apply Gaussian Blur
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Binarization using Sauvola thresholding
    thresh_sauvola = threshold_sauvola(blurred, window_size=25)
    binary_sauvola = (blurred > thresh_sauvola).astype(np.uint8) * 255
    
    # Apply Morphological operations
    kernel = np.ones((1, 1), np.uint8)
    erosion = cv2.erode(binary_sauvola, kernel, iterations=1)
    dilation = cv2.dilate(erosion, kernel, iterations=1)
    
    # Apply adaptive thresholding for binary conversion
    adaptive_thresh = cv2.adaptiveThreshold(dilation, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                            cv2.THRESH_BINARY, 11, 2)
    
    # Apply Morphological operations
    kernel = np.ones((2, 2), np.uint8)
    erosion = cv2.erode(adaptive_thresh, kernel, iterations=3)
    dilation = cv2.dilate(erosion, kernel, iterations=1)
    
    #OCR section 
    config = "--oem 3 --psm 6"
    ocr_text=py.image_to_string(dilation, config=config, lang='eng')

    save_folder = "media/processed_img/"
    img_path=os.path.join(save_folder, image_Name)
    cv2.imwrite(img_path,dilation)

    return ocr_text


