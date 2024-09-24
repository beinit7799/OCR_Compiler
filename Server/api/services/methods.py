import cv2 
import numpy as np

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
def allowed_file(filename):
    if '.' in filename:
        base_name, extension = filename.rsplit('.', 1)
        extension = extension.lower()
        
        if extension in ALLOWED_EXTENSIONS:
            return True
    return False

def img_Processing(img):
    # Grayscale
    gray_img=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    
    # Noise Removal
    gray_img = cv2.bilateralFilter(gray_img,20,30,30)

    # Binarization
    img_bw = cv2.adaptiveThreshold(gray_img,255,cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY,9,3)

    # Morph
    kernal = np.ones((3,2),np.uint8)
    op = cv2.morphologyEx(img_bw,cv2.MORPH_OPEN,kernal)
    
    # Thickening
    er=cv2.erode(op,kernal,iterations=1)
    return er
    
# Rescale
def rescaleFrame(frame,scale=0.5): 
    width = int(frame.shape[1]*scale) 
    height = int(frame.shape[0]*scale)
    dimensions = (width,height)
    return cv2.resize(frame , dimensions , interpolation=cv2.INTER_AREA)


# Contures detection
def contures_detection(edged,img):
    # img_temp = img.copy()
    def biggest_contour(contours):
        biggest = np.array([])
        max_area = 0
        for i in contours:
            area = cv2.contourArea(i)
            if area > 100:
                peri = cv2.arcLength(i,True)
                approx = cv2.approxPolyDP(i,0.015*peri,True)
                if area>max_area and len(approx)== 4:
                    biggest = approx
                    max_area=area
        return biggest 
    
    contours, hierarchy = cv2.findContours(edged,cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours,key=cv2.contourArea,reverse=True)[:10]

    biggest = biggest_contour(contours)
    
    if len(biggest) == 0:
        return img
    else:
        # For testing
        # cv2.drawContours(img_temp, [biggest], -1, (0, 255, 0), 5)
        # cv2.imshow('contour',img_temp)
        
        #Prespective transformation
        points = biggest.reshape(4, 2)
        input_points = np.zeros((4, 2), dtype="float32")

        points_sum = points.sum(axis=1)
        input_points[0] = points[np.argmin(points_sum)]
        input_points[3] = points[np.argmax(points_sum)]

        points_diff = np.diff(points, axis=1)
        input_points[1] = points[np.argmin(points_diff)]
        input_points[2] = points[np.argmax(points_diff)]

        (top_left, top_right, bottom_right, bottom_left) = input_points
        bottom_width = np.sqrt(((bottom_right[0] - bottom_left[0]) ** 2) + ((bottom_right[1] - bottom_left[1]) ** 2))
        top_width = np.sqrt(((top_right[0] - top_left[0]) ** 2) + ((top_right[1] - top_left[1]) ** 2))
        right_height = np.sqrt(((top_right[0] - bottom_right[0]) ** 2) + ((top_right[1] - bottom_right[1]) ** 2))
        left_height = np.sqrt(((top_left[0] - bottom_left[0]) ** 2) + ((top_left[1] - bottom_left[1]) ** 2))

        # Output image size
        max_width = max(int(bottom_width), int(top_width))
        # max_height = max(int(right_height), int(left_height))
        max_height = int(max_width * 1.414)  # for A4

        # Desired points values in the output image
        converted_points = np.float32([[0, 0], [max_width, 0], [0, max_height], [max_width, max_height]])

        # Perspective transformation
        matrix = cv2.getPerspectiveTransform(input_points, converted_points)
        img_output = cv2.warpPerspective(img, matrix, (max_width, max_height))
        
        return img_output
