
import speech_recognition as sr
from datetime import datetime, timedelta
import pandas as pd
import os
from dotenv import load_dotenv
import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext

import threading
import audioop
import queue

try:
    import winsound
except:
    pass

mic_names = sr.Microphone.list_microphone_names()
print(mic_names)

def get_mic_index(mic_name):
    try:
        return mic_names.index(mic_name)
    except ValueError:
        print(f"Microphone '{mic_name}' not found.")
        return None

def monitor_audio(mic_index, audio_queue):
    with sr.Microphone(device_index=mic_index) as source:
        r = sr.Recognizer()
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)  # Adjust for ambient noise once, before starting the loop
        while not stop_threads:
            with sr.Microphone(device_index=mic_index) as source:
                audio_data = r.listen(source, phrase_time_limit=1)
                audio_queue.put(audio_data)

def update_audio_levels():
    while not stop_threads:
        if not audio_queue.empty():
            audio_data = audio_queue.get()
            # Convert audio to raw data to calculate RMS (audio levels)
            raw_data = audio_data.get_raw_data()
            rms = audioop.rms(raw_data, 2)  # 2 is for stereo
            audio_level_var.set(f"Audio Level: {rms}")
        root.after(100, update_audio_levels)  # Update the label every 100ms

def record_speech():

    speech_mic_name = tag_var.get()
    speech_mic_index = get_mic_index(speech_mic_name)

    r = sr.Recognizer()
    mic = sr.Microphone(device_index=speech_mic_index)
    if os.name == 'nt':
        winsound.Beep(1000, 500)
    print("\n\n [ Recording in progress ] \n\n")
    
    with mic as source:
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
    
    if os.name == 'nt':
        winsound.Beep(700, 400)
    current_time = datetime.now().strftime("%H:%M:%S")
    try:
        speech = r.recognize_google(audio)
    except sr.UnknownValueError:
        print("[Could not understand audio]\n")
    except sr.RequestError as e:
        print("[Could not understand audio]")


    text_area.insert(tk.END, f"{current_time} - {speech}\n", "color")
    text_area.see(tk.END)
    return speech, current_time

def main():
    speech, current_time = record_speech()
    print('\n\n', speech, '\n\n')
    print(f"Current Time: {current_time}")

def main_gui():
    global stop_threads, audio_queue, audio_level_var
    stop_threads = False
    audio_queue = queue.Queue()

    root = tk.Tk()
    root.title("Microphone Setup")
    
    audio_level_var = tk.StringVar()
    audio_level_label = tk.Label(root, textvariable=audio_level_var)
    audio_level_label.grid(row=3, column=0, columnspan=3)

    # Your existing GUI setup here...
    # Dropdown, buttons, etc.
    text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD)
    text_area.grid(row=0, column=0, columnspan=3, pady=10)  # Spanning across three columns

    tag_var = tk.StringVar()
    dropdown = ttk.Combobox(root, textvariable=tag_var, values=mic_names, width=40)
    dropdown.grid(row=1, column=1, columnspan=2, pady=5)  # Spanning across three columns
    dropdown.set('Select a microphone')

    record_btn = tk.Button(root, text="Test", command=main)
    record_btn.grid(row=2, column=0, pady=5, sticky='ew')

    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)
    root.grid_columnconfigure(2, weight=1)


    mic_index = get_mic_index(tag_var.get())
    if mic_index is not None:
        threading.Thread(target=monitor_audio, args=(mic_index, audio_queue), daemon=True).start()
        root.after(100, update_audio_levels)  # Start updating the GUI with audio levels

    root.protocol("WM_DELETE_WINDOW", on_closing)  # Handle window closing
    root.mainloop()

def on_closing():
    global stop_threads
    stop_threads = True
    root.destroy()

if __name__ == "__main__":
    main_gui()

