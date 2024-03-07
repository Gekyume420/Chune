import tkinter as tk
from tkinter import scrolledtext
import speech_recognition as sr
from datetime import datetime
import os
import winsound 

# Initialize the main window
root = tk.Tk()
root.title("Speech to Text")

# Variable to hold the state of the checkbox
color_var = tk.IntVar()

# Define the function to record and display speech
def record_speech():
    r = sr.Recognizer()
    mic = sr.Microphone()
    if os.name == 'nt':
        winsound.Beep(1000, 500)  # Start beep for Windows
    
    with mic as source:
        audio = r.listen(source)
    
    if os.name == 'nt':
        winsound.Beep(700, 400)  # End beep for Windows
    current_time = datetime.now().strftime("%H:%M:%S")
    try:
        speech = r.recognize_google(audio)
        print(speech)
    except sr.UnknownValueError:
        speech = "[Could not understand audio]"
    except sr.RequestError as e:
        speech = "[Could not request results; {0}]".format(e)
    
    # Check if the checkbox is checked for red text
    if color_var.get() == 1:
        text_color = "red"
    else:
        text_color = "black"
    
    # Configure and insert text with specific color
    text_area.tag_configure("color", foreground=text_color)
    text_area.insert(tk.END, f"{current_time} - {speech}\n", "color")
    text_area.see(tk.END)

# Create scrolled text area for displaying the speech
text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD)
text_area.pack(pady=10)

# Create a button to start recording
record_btn = tk.Button(root, text="Record Speech", command=record_speech)
record_btn.pack(side=tk.LEFT, pady=5)

# Create a check button for selecting red text output
check_btn = tk.Checkbutton(root, text="Red Text", variable=color_var)
check_btn.pack(side=tk.RIGHT, padx=10)

# Run the GUI main loop
root.mainloop()