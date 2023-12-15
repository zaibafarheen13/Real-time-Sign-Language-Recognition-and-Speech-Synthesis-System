# Importing the Libraries Required
import cv2
import os

# Creating and Collecting Training Data
mode = 'testingData'
directory = 'dataSet/' + mode + '/'
minValue = 35

capture = cv2.VideoCapture(0)
interrupt = -1

while True:
    _, frame = capture.read()

    # Simulating mirror Image
    frame = cv2.flip(frame, 1)

    # Getting count of existing images
    count = {}
    for char in 'abcdefghijklmnopqrstuvwxyz0123456789':
        count[char] = len(os.listdir(directory + char.upper()))

    # Printing the count of each set on the screen
    for char in 'abcdefghijklmnopqrstuvwxyz0123456789':
        cv2.putText(frame, f"{char} : {count[char]}", (10, 60 + (ord(char) - ord('a')) * 10), cv2.FONT_HERSHEY_PLAIN, 1, (0,255,255), 1)

    # Coordinates of the ROI
    x1, y1, x2, y2 = int(0.5 * frame.shape[1]), 10, frame.shape[1] - 10, int(0.5 * frame.shape[1])

    # Drawing the ROI
    cv2.rectangle(frame, (x1-1, y1-1), (x2+1, y2+1), (255,0,0) ,1)

    # Extracting the ROI
    roi = frame[y1:y2, x1:x2]

    cv2.imshow("Frame", frame)

    # Image Processing
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5), 2)
    th3 = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
    ret, test_image = cv2.threshold(th3, minValue, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

    # Output Image after the Image Processing that is used for data collection 
    test_image = cv2.resize(test_image, (300,300))
    cv2.imshow("test", test_image)

    # Data Collection
    interrupt = cv2.waitKey(10)
    if interrupt & 0xFF == 27:  # esc key
        break

    # Capture and save images for each letter and number if the corresponding key is pressed
    for char in 'abcdefghijklmnopqrstuvwxyz0123456789':
        if interrupt & 0xFF == ord(char):
            cv2.imwrite(directory + char.upper() + '/' + str(count[char]) + '.jpg', roi)

capture.release()
cv2.destroyAllWindows()
