import cv2
import numpy as np
import os

# Creating and Collecting Training Data
mode = 'trainingData'
directory = 'dataSet/' + mode + '/'
minValue = 70

# Open the webcam
capture = cv2.VideoCapture(0)
interrupt = -1

while True:
    # Read a frame from the webcam
    _, frame = capture.read()
    # Flip the frame horizontally to simulate a mirror image
    frame = cv2.flip(frame, 1)

    # Count the number of existing images for each letter and number
    count = {}
    for char in 'abcdefghijklmnopqrstuvwxyz0123456789':
        count[char] = len(os.listdir(directory + char.upper()))

    # Display the count of images for each letter and number on the frame
    for char in 'abcdefghijklmnopqrstuvwxyz0123456789':
        cv2.putText(frame, f"{char} : {count[char]}", (10, 60 + (ord(char) - ord('a')) * 10), cv2.FONT_HERSHEY_PLAIN, 1, (0,255,255), 1)

    # Define the coordinates of the Region of Interest (ROI)
    x1, y1, x2, y2 = int(0.5 * frame.shape[1]), 10, frame.shape[1] - 10, int(0.5 * frame.shape[1])
    # Draw a rectangle around the ROI
    cv2.rectangle(frame, (x1-1, y1-1), (x2+1, y2+1), (255,0,0), 1)
    
    # Extract the ROI
    roi = frame[y1:y2, x1:x2]

    # Display the frame with the ROI
    cv2.imshow("Frame", frame)

    # Image processing on the ROI
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5), 2)
    th3 = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
    ret, test_image = cv2.threshold(th3, minValue, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

    # Display the processed image
    test_image = cv2.resize(test_image, (300,300))
    cv2.imshow("test", test_image)

    # Wait for a key press
    interrupt = cv2.waitKey(10)
    if interrupt & 0xFF == 27:  # Break the loop if the 'esc' key is pressed
        break
    
    # Capture and save images for each letter and number if the corresponding key is pressed
    for char in 'abcdefghijklmnopqrstuvwxyz0123456789':
        if interrupt & 0xFF == ord(char):
            cv2.imwrite(directory + char.upper() + '/' + str(count[char]) + '.jpg', roi)

# Release the webcam and close all windows
capture.release()
cv2.destroyAllWindows()
