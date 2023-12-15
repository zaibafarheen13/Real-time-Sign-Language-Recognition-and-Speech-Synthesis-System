# Import necessary libraries
import numpy as np
import cv2
import os

# Import the 'func' function from a module named 'image_processing'
from image_processing import func

# Set the data, train, and test folder locations
data_folder = "C:/Users/zaiba/Documents/Final_CoC/dataSet"
train_folder = "C:/Users/zaiba/Documents/Final_CoC/dataSet/trainingData"
test_folder = "C:/Users/zaiba/Documents/Final_CoC/dataSet/testingData"

# Create directories if they don't exist
if not os.path.exists(data_folder):
    os.makedirs(data_folder)
if not os.path.exists(train_folder):
    os.makedirs(train_folder)
if not os.path.exists(test_folder):
    os.makedirs(test_folder)

# Set paths
path = train_folder
path1 = data_folder
a = ['label']

# Add pixel column names to the list
for i in range(64 * 64):
    a.append("pixel" + str(i))

# Initialize variables
label = 0
var = 0
c1 = 0
c2 = 0

# Loop through directories and process images
for (dirpath, dirnames, filenames) in os.walk(path):
    for dirname in dirnames:
        print(dirname)

        # Loop through subdirectories and process image files
        for (direcpath, direcnames, files) in os.walk(path + "/" + dirname):
            if not os.path.exists(path1 + "/trainingData/" + dirname):
                os.makedirs(path1 + "/trainingData/" + dirname)
            if not os.path.exists(path1 + "/testingData/" + dirname):
                os.makedirs(path1 + "/testingData/" + dirname)

            # Use all images for both training and testing
            num = len(files)

            for file in files:
                var += 1
                actual_path = path + "/" + dirname + "/" + file
                actual_path1 = path1 + "/trainingData/" + dirname + "/" + file
                actual_path2 = path1 + "/testingData/" + dirname + "/" + file

                # Read the image and apply preprocessing using the 'func' function
                img = cv2.imread(actual_path, 0)
                bw_image = func(actual_path)

                # Save the images to both training and testing folders
                cv2.imwrite(actual_path1, bw_image)
                cv2.imwrite(actual_path2, bw_image)

        label = label + 1

# Print statistics
print("Total images:", var)
print("Training set size:", var)
print("Testing set size:", var)
