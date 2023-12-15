# Import necessary libraries
import numpy as np
import cv2

# Set a minimum value for thresholding
minValue = 70

# Define a function named 'func' that takes a file path as an argument
def func(path):    
    # Read an image from the specified file path
    frame = cv2.imread(path)
    
    # Convert the image to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Apply Gaussian blur to the grayscale image
    blur = cv2.GaussianBlur(gray, (5, 5), 2)

    # Apply adaptive thresholding to the blurred image
    th3 = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
    
    # Apply thresholding using Otsu's method to the result of adaptive thresholding
    ret, res = cv2.threshold(th3, minValue, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    
    # Return the resulting image after thresholding
    return res
