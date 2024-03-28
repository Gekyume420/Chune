import speech_recognition as sr
from datetime import datetime
import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
import threading
import queue
import audioop

import pyaudio
import numpy as np

try:
    import winsound
except ImportError:
    pass

# Fetch the list of microphone names
mic_names = sr.Microphone.list_microphone_names()

def get_mic_index(mic_name):
    try:
        return mic_names.index(mic_name)
    except ValueError:
        print(f"Microphone '{mic_name}' not found.")
        return None

def monitor_audio_level(queue, stop_event):
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=44100,
                    input=True,
                    frames_per_buffer=1024)

    while not stop_event.is_set():
        try:
            data = np.frombuffer(stream.read(1024), dtype=np.int16)
            audio_level = np.sqrt(np.mean(data**2))
            queue.put(audio_level)
        except Exception as e:
            print(f"Error reading audio level: {e}")
            break
    
    stream.stop_stream()
    stream.close()
    p.terminate()

def update_audio_level(queue, stop_event, label_var):
    while not stop_event.is_set():
        try:
            level = queue.get_nowait()
            label_var.set(f"Audio Level: {level}")
        except queue.empty:
            pass
def start_monitoring():
    stop_event.clear()
    threading.Thread(target=monitor_audio_level, args=(audio_level_queue, stop_event), daemon=True).start()
    threading.Thread(target=update_audio_level, args=(audio_level_queue, stop_event, audio_level_var), daemon=True).start()



root = tk.Tk()
root.title("Microphone Setup")

audio_level_queue = queue.Queue()
stop_event = threading.Event()
audio_level_var = tk.StringVar(root, value="Audio Level: ")

text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD)
text_area.grid(row=0, column=0, columnspan=3, pady=10)

tag_var = tk.StringVar()
dropdown = ttk.Combobox(root, textvariable=tag_var, values=mic_names)
dropdown.grid(row=1, column=1, pady=5)
dropdown.set('Select a microphone')

record_btn = tk.Button(root, text="Start Monitoring", command=start_monitoring)
record_btn.grid(row=2, column=0, pady=5, sticky='ew')

audio_level_label = tk.Label(root, textvariable=audio_level_var)
audio_level_label.grid(row=3, column=0, columnspan=3)

root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)

root.mainloop()