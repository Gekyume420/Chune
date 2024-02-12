import speech_recognition as sr
import time
import winsound
from datetime import datetime
import pandas as pd

r = sr.Recognizer()

filename = '2-12-24.csv'

def delete_last_entry(df, filename):
    if not df.empty:
        df = df[:-1]  # Remove the last row
        df.to_csv(filename, index=False)
        print("Last entry deleted from the CSV file.")
    else:
        print("CSV file is empty. No entries to delete.")

def calculate_task_duration(df):
    # Check if there is at least one 'start task' entry
    start_task_entries = df[df['Python'].str.contains('start task', na=False, case=False)]
    if not start_task_entries.empty:
        # Get the timestamp of the last 'start task' entry
        last_start_task_time = pd.to_datetime(start_task_entries['Timestamp'].iloc[-1])

        # Get the current time
        current_time = datetime.now()

        # Calculate the duration
        duration = current_time - last_start_task_time
        return duration.total_seconds()

    return None


df = pd.read_csv(filename)

mic = sr.Microphone()

# you are good to record beep
winsound.Beep(1000, 500)

with mic as source:
    audio = r.listen(source)

# recording has finished beep
winsound.Beep(700, 400)
# recording session info
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
speech = r.recognize_google(audio)

# Check if the word "delete" is spoken
if speech == 'delete last row':
    delete_last_entry(df, filename)
    print("Deletion logic executed.")



if 'end task' in speech.lower():
    print("Task Time Counter Stopped")
    speech = speech.lower()
    new_data2 = {'Timestamp': [current_time], 'Python': [speech]}
    df_new2 = pd.DataFrame(new_data2)
    df = pd.concat([df, df_new2], ignore_index=True)
    df.to_csv(filename, index=False)

    # Calculate the duration and log it
    duration_seconds = calculate_task_duration(df)
    if duration_seconds is not None:
        print(f"Task duration: {duration_seconds} seconds")

else:
    # Check if the length of speech is greater than 100 characters
    if len(speech) > 100:
        first_of_data = speech[:100]
        rest_of_data = speech[100:]

        # Append new data to the DataFrame
        new_data = {'Timestamp': [current_time], 'Python': [first_of_data]}
        df_new = pd.DataFrame(new_data)
        df = pd.concat([df, df_new], ignore_index=True)

        new_data2 = {'Timestamp': '', 'Python': [rest_of_data]}
        df_new2 = pd.DataFrame(new_data2)
        df = pd.concat([df, df_new2], ignore_index=True)

    else:
        new_data2 = {'Timestamp': [current_time], 'Python': [speech]}
        df_new2 = pd.DataFrame(new_data2)
        df = pd.concat([df, df_new2], ignore_index=True)

    # Write the updated DataFrame back to the CSV file
    df.to_csv(filename, index=False)

print(speech)
print(f"Current Time: {current_time}")
