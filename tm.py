import speech_recognition as sr
import time
import winsound
from datetime import datetime
import pandas as pd

r = sr.Recognizer()

filename = '2-12-24.csv'

def format_sentence(sentence, words_per_line=10):
    formatted_sentence = []
    for i, word in enumerate(sentence.split()):
        formatted_sentence.append(word)
        if i != 0 and i % words_per_line == 0:
            formatted_sentence.append("\n")
    return " ".join(formatted_sentence)

def delete_last_entry(df):
    if not df.empty:
        df = df[:-1]  # Remove the last row
        print("Last entry deleted from the CSV file.")
        return df
    else:
        print("CSV file is empty. No entries to delete.")

def calculate_task_duration(df):
    # Check if there is at least one 'start task' entry
    start_task_entries = df[df['task'].str.contains('start task', na=False, case=False)]
    if not start_task_entries.empty:
        # Get the timestamp of the last 'start task' entry
        last_start_task_time = pd.to_datetime(start_task_entries['time'].iloc[-1])

        # Get the current time
        current_time = datetime.now()

        # Calculate the duration
        duration = current_time - last_start_task_time
        return duration.total_seconds()

    return None

def record_speech():
    mic = sr.Microphone()
    winsound.Beep(1000, 500)
    with mic as source:
        audio = r.listen(source)
    winsound.Beep(700, 400)
    # recording session info
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    speech = r.recognize_google(audio)

    return speech, current_time

def add_row(df, speech, current_time):
    df2 = pd.DataFrame({'time': [current_time], 'task': [speech]})
    df = pd.concat([df, df2], ignore_index=True)
    return df

def execute_task(df, speech, current_time):
    speech = format_sentence(speech)
    # Check if the word "delete" is spoken
    if speech == 'delete last row':
        df = delete_last_entry(df, filename)
        print("Deletion logic executed.")

    if speech.lower().startswith("start task"):
        df = add_row(df, speech, current_time)

    elif speech.lower().startswith("end task"):
        print("Task Time Counter Stopped")
        df = add_row(df, "task ended", current_time)

        # Calculate the duration and log it
        duration_seconds = calculate_task_duration(df)
        if duration_seconds is not None:
            print(f"Task duration: {duration_seconds} seconds")
    else:
        df = add_row(df, speech, current_time) 
        
    return df



def write_task(df, filename):
    df.to_csv(filename, index=False)

# delete last task entry
# start a task
# end a task
    
if __name__ == "__main__":
    df = pd.read_csv(filename)
    speech, current_time = record_speech()
    data = execute_task(df, speech, current_time)
    write_task(data, filename)

print(speech)
print(f"Current Time: {current_time}")
