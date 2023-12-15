# Importing Libraries
import numpy as np
import cv2
import os
import operator
from string import ascii_uppercase
import tkinter as tk
from tkinter import font
from PIL import Image, ImageTk
from hunspell import Hunspell
from keras.models import model_from_json
import pyttsx3

screen_width = 0  # Variable to store the screen width

# Application class
class Application:
    def __init__(self):
        # Initialize Hunspell for spell checking
        self.hs = Hunspell('en_US')

        # Initialize video capture from the default camera (index 0)
        self.vs = cv2.VideoCapture(0)

        # Load the pre-trained model from disk
        self.json_file = open("models/model2.json", "r")
        self.model_json = self.json_file.read()
        self.json_file.close()
        self.loaded_model = model_from_json(self.model_json)
        self.loaded_model.load_weights("models/model2.h5")

        # Initialize counters and flags for gesture recognition
        self.ct = {}
        self.ct['blank'] = 0
        self.blank_flag = 0

        # Initialize counters for each uppercase letter
        for i in ascii_uppercase:
            self.ct[i] = 0

        print("Loaded model from disk")

        # Initialize the Tkinter GUI window
        self.root = tk.Tk()
        self.root.protocol('WM_DELETE_WINDOW', self.destructor)
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"{screen_width}x{screen_height}+0+0")

        # Initialize Tkinter labels and buttons
        self.root.title("Real-time Sign Language and Speech Synthesis")

        # Create Canvas for the heading and gradient text
        self.canvas = tk.Canvas(self.root, bg="white", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Create conic gradient text
        self.create_conic_gradient_text("Real-time Sign Language and Speech Synthesis", ["#553c9a", "#ee4b2b", "#00c2cb"])

        # Tkinter labels for displaying information
        self.panel3 = tk.Label(self.root, font=("Poppins ExtraBold", 20, "bold"), fg="red", bg="white")  # Current Symbol
        self.panel3.place(x=590, y=560)

        self.T1 = tk.Label(self.root)
        self.T1.place(x=450, y=560)
        self.T1.config(text="Character :", font=("Poppins", 15, "bold"), fg="orange", bg="white")

        self.panel4 = tk.Label(self.root)  # Word
        self.panel4.place(x=540, y=590)
        self.panel4.config(font=("Poppins ExtraBold", 15, "bold"), fg="red", bg="white")

        self.T2 = tk.Label(self.root)
        self.T2.place(x=450, y=590)
        self.T2.config(text="Word :", font=("Poppins", 15, "bold"), fg="orange", bg="white")

        self.panel5 = tk.Label(self.root)  # Sentence
        self.panel5.place(x=570, y=615)
        self.panel5.config(font=("Poppins ExtraBold", 15, "bold"), fg="red", bg="white")

        self.T3 = tk.Label(self.root)
        self.T3.place(x=450, y=620)
        self.T3.config(text="Sentence :", font=("Poppins", 15, "bold"), fg="orange", bg="white")

        self.T4 = tk.Label(self.root)
        self.T4.place(x=450, y=660)
        self.T4.config(text="Suggestions :", fg="red", font=("Poppins", 20, "bold"), bg="white")

        self.panel = tk.Label(self.root)
        self.panel.place(x=450, y=60, width=580, height=480)

        self.panel2 = tk.Label(self.root)  # initialize image panel
        self.panel2.place(x=650, y=80, width=350, height=350)

        # Initialize Tkinter buttons for word suggestions
        button_width = 14  # Adjust the button width
        button_gap = 10  # Adjust the gap between buttons

        # Add buttons below the "Suggestions" label
        button_width = 220
        button_height = 35
        label_x = 500
        label_y = 690
        button1_x = label_x
        button2_x = label_x + button_width + 10  # Add spacing between buttons
        button3_x = label_x + 2 * (button_width + 10)  # Add spacing between buttons

        # Create buttons with permanent red border
        self.bt1 = self.create_styled_button("Suggestion-1", label_x + 140, label_y - 31, button_width, button_height,
                                             1, font_color="red")
        self.bt2 = self.create_styled_button("Suggestion-2", button2_x + 150, label_y - 31, button_width, button_height,
                                             2, font_color="red")
        self.bt3 = self.create_styled_button("Suggestion-3", button3_x + 160, label_y - 31, button_width, button_height,
                                             3, font_color="red")
        # Larger size and bigger font for Clear, Backspace, and Speak buttons
        larger_button_width = 250
        larger_button_height = 45
        self.bt_backspace = self.create_styled_button("Backspace", label_x - 120, label_y + 30, larger_button_width,
                                                      larger_button_height, 4, font_color="#1E90FF")
        self.bt_clear = self.create_styled_button("Clear", button2_x - 60, label_y + 30, larger_button_width,
                                                   larger_button_height, 5, font_color="#1E90FF")
        self.bt_finish = self.create_styled_button("Speak", button3_x, label_y + 30, larger_button_width,
                                                    larger_button_height, 6, font_color="#1E90FF")

        # Initialize variables for storing recognized symbols and words
        self.str = ""
        self.word = " "
        self.current_symbol = "Empty"
        self.photo = "Empty"

        # Initialize flag to track finishing
        self.finish_flag = False

        # Start the video loop to capture frames and update the GUI
        self.video_loop()

    def create_styled_button(self, text, x_position, y_position, width, height, action, font_color="red"):
        # Function to create a styled button
        global screen_width
        # Adjust highlightthickness based on font color
        highlightthickness_value = 1 if font_color == "red" else 3
        button = tk.Button(
            self.root,
            text=text,
            font=("Bold", 14),  # Larger font size
            fg=font_color,  # Set the font color
            bg='white',  # Set the background color to white
            bd=1,  # Set the border width to 1 to create a dark blue border
            padx=5,  # Add padding
            pady=5,  # Add padding
            relief=tk.SOLID,  # Set the relief to SOLID to create a solid border
            activebackground='white',  # Set active background to white
            activeforeground=font_color,  # Set active foreground to the specified font color
            highlightthickness=highlightthickness_value,  # Set the highlight thickness
            borderwidth=0,
            highlightbackground=font_color,  # Set the highlight background to the specified font color
        )
        if action == 1:
            button.config(command=self.action1)
        elif action == 2:
            button.config(command=self.action2)
        elif action == 3:
            button.config(command=self.action3)
        elif action == 4:
            button.config(command=self.backspace_action)
        elif action == 5:
            button.config(command=self.clear_action)
        elif action == 6:
            button.config(command=self.finish_action)

        button.place(x=x_position, y=y_position, width=width, height=height)
        return button

    def create_conic_gradient_text(self, text, colors):
        # Function to create conic gradient text
        global screen_width  # Declare screen_width as a global variable
        width = self.canvas.winfo_reqwidth()
        height = self.canvas.winfo_reqheight()

        words = text.split()  # Split the text into words
        num_words = len(words)
        num_colors = len(colors)

        total_width = sum(self.text_width(word) for word in words) + (len(words) - 1) * self.text_width(' ')

        # Calculate the starting x position to center the words
        start_x = (screen_width - total_width) / 2 + 750
        start_y = height / 19  # Adjust this value to move the heading up or down

        for i, word in enumerate(words):
            color = colors[i % num_colors]

            # Create text with conic gradient fill
            self.canvas.create_text(
                start_x, start_y,
                text=word,
                font=("Helvetica", 24, "bold"),
                fill=color,
                anchor=tk.NW,
            )

            # Update the starting x position for the next word
            start_x += self.text_width(word) + self.text_width(' ')

    def text_width(self, text):
        # Function to calculate the width of a text string
        font_object = font.Font(family="Helvetica", size=24, weight="bold")
        return font_object.measure(text)

    def video_loop(self):
        # Main video loop for capturing frames and updating the GUI
        ok, frame = self.vs.read()

        if ok:
            # Flip the frame horizontally
            cv2image = cv2.flip(frame, 1)

            # Define region of interest (ROI) for hand gesture recognition
            x1 = int(0.5 * frame.shape[1])
            y1 = 10
            x2 = frame.shape[1] - 10
            y2 = int(0.5 * frame.shape[1])

            # Draw a rectangle around the ROI
            cv2.rectangle(frame, (x1 - 1, y1 - 1), (x2 + 1, y2 + 1), (255, 0, 0), 1)

            # Convert the frame to RGBA format for displaying in Tkinter
            cv2image = cv2.cvtColor(cv2image, cv2.COLOR_BGR2RGBA)

            # Display the current frame in the Tkinter GUI
            self.current_image = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=self.current_image)
            self.panel.imgtk = imgtk
            self.panel.config(image=imgtk)

            # Crop the region of interest (ROI) from the frame for gesture recognition
            cv2image = cv2image[y1: y2, x1: x2]

            # Convert the ROI to grayscale and apply image processing
            gray = cv2.cvtColor(cv2image, cv2.COLOR_BGR2GRAY)
            blur = cv2.GaussianBlur(gray, (5, 5), 2)
            th3 = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
            ret, res = cv2.threshold(th3, 70, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

            # Perform gesture recognition and update the GUI
            self.predict(res)

            # Display the processed image in the Tkinter GUI
            self.current_image2 = Image.fromarray(res)
            imgtk = ImageTk.PhotoImage(image=self.current_image2)
            self.panel2.imgtk = imgtk
            self.panel2.config(image=imgtk)

            # Update Tkinter labels with recognized symbols and words
            self.panel3.config(text=self.current_symbol, font=("Poppins Light", 14))
            self.panel4.config(text=self.word, font=("Poppins Light", 14))
            self.panel5.config(text=self.str, font=("Poppins Light", 14))

            # Get word suggestions from the Hunspell spell checker
            predicts = self.hs.suggest(self.word)

            # Update Tkinter buttons with word suggestions
            if len(predicts) > 1:
                self.bt1.config(text=predicts[0], font=("Poppins Light", 14))
            else:
                self.bt1.config(text="")

            if len(predicts) > 2:
                self.bt2.config(text=predicts[1], font=("Poppins Light", 14))
            else:
                self.bt2.config(text="")

            if len(predicts) > 3:
                self.bt3.config(text=predicts[2], font=("Poppins Light", 14))
            else:
                self.bt3.config(text="")

            # Speak the current sentence if the finish flag is set
            if self.finish_flag:
                self.speak_sentence(self.str)
                self.finish_flag = False

        # Call the video loop function after a delay (5 milliseconds)
        self.root.after(5, self.video_loop)

    def predict(self, test_image):
        # Function to perform gesture recognition and update the GUI
        # Resize the test image to match the model's input size
        test_image = cv2.resize(test_image, (128, 128))

        # Perform prediction using the loaded model
        result = self.loaded_model.predict(test_image.reshape(1, 128, 128, 1))

        # Map the model's output to corresponding symbols
        prediction = {}
        prediction['blank'] = result[0][0]
        inde = 1

        for i in ascii_uppercase:
            prediction[i] = result[0][inde]
            inde += 1

        # Sort the predictions in descending order
        prediction = sorted(prediction.items(), key=operator.itemgetter(1), reverse=True)

        # Get the most probable symbol as the current symbol
        self.current_symbol = prediction[0][0]

                # Reset counters if the current symbol is 'blank'
        if self.current_symbol == 'blank':
            for i in ascii_uppercase:
                self.ct[i] = 0

        # Update the counter for the current symbol
        self.ct[self.current_symbol] += 1

        # Check for gesture recognition based on counters
        if self.ct[self.current_symbol] > 60:
            for i in ascii_uppercase:
                if i == self.current_symbol:
                    continue
                tmp = self.ct[self.current_symbol] - self.ct[i]

                if tmp < 0:
                    tmp *= -1

                # Check if the difference in counters is within a threshold
                if tmp <= 20:
                    self.ct['blank'] = 0

                    for i in ascii_uppercase:
                        self.ct[i] = 0
                    return

            self.ct['blank'] = 0

            for i in ascii_uppercase:
                self.ct[i] = 0

            # Process recognized symbols and words
            if self.current_symbol == 'blank':
                if self.blank_flag == 0:
                    self.blank_flag = 1

                    if len(self.str) > 0:
                        self.str += " "

                    self.str += self.word

                    self.word = ""
            else:
                if len(self.str) > 16:
                    self.str = ""

                self.blank_flag = 0
                self.word += self.current_symbol

    def action1(self):
        # Button action for word suggestion 1
        predicts = self.hs.suggest(self.word)
        if len(predicts) > 0:
            self.word = ""
            self.str += " "
            self.str += predicts[0]

    def action2(self):
        # Button action for word suggestion 2
        predicts = self.hs.suggest(self.word)
        if len(predicts) > 1:
            self.word = ""
            self.str += " "
            self.str += predicts[1]

    def action3(self):
        # Button action for word suggestion 3
        predicts = self.hs.suggest(self.word)
        if len(predicts) > 2:
            self.word = ""
            self.str += " "
            self.str += predicts[2]

    def backspace_action(self):
        # Button action for the "Backspace" button
        if len(self.word) > 0:
            self.word = self.word[:-1]

    def finish_action(self):
        # Button action for the "Finish" button
        self.finish_flag = True

    def clear_action(self):
        # Button action for the "Clear" button
        self.str = ""
        self.word = ""

    def speak_sentence(self, sentence):
        # Speak the given sentence using text-to-speech
        engine = pyttsx3.init()
        engine.say(sentence)
        engine.runAndWait()

    def destructor(self):
        # Close the application
        print("Closing Application...")
        self.root.destroy()
        self.vs.release()
        cv2.destroyAllWindows()

# Main entry point
print("Starting Application...")
(Application()).root.mainloop()

