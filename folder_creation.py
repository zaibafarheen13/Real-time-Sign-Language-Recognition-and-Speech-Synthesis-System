# Importing the Libraries Required
import os
import string

# Creating the directory Structure

if not os.path.exists("dataSet"):
    os.makedirs("dataSet")

# Creating folders for training and testing data
for data_type in ['trainingData', 'testingData']:
    data_path = os.path.join("dataSet", data_type)
    if not os.path.exists(data_path):
        os.makedirs(data_path)

    # Making folders for 0-9 and A-Z in the training and testing data folders respectively
    for char in string.digits + string.ascii_uppercase:
        char_path = os.path.join(data_path, char)
        if not os.path.exists(char_path):
            os.makedirs(char_path)
