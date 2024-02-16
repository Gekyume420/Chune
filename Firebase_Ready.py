import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import speech_recognition as sr
import time
import winsound
from datetime import datetime
import pandas as pd
# Path to your Firebase Admin SDK private key
cred = credentials.Certificate('C:/Users/16198/Desktop/FIREBASE/chunelink-firebase-adminsdk-unh7l-267bbbcfac.json')
# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {'databaseURL': 'https://chunelink-default-rtdb.firebaseio.com/'})

# Static unique identifier
COMPUTER_ID = "Jackson"  # Change this to "id_nicks_computer" on Nick's computer


"""
            Firebase commands [Below]

"""

def add_row_firebase(data):
    # Reference to your Firebase database path
    ref = db.reference(f'/tasks/{COMPUTER_ID}')
    #ref = db.reference('/tasks')
    # Pushes a new entry onto the database
    ref.push(data)

def execute_task_firebase(df, speech, current_time):
    # Your existing logic here
   
    # Instead of adding to a local DataFrame, push to Firebase
    data = {'time': current_time, 'task': speech}
    # Depending on the condition, you might want to add more to `data`
    add_row_firebase(data)

"""

#This function will print out new tasks as they're added to the database. You can adapt it to merge new entries into your local CSV file or take any other action needed.
def listen_for_changes():
    # Listen for changes only in the specific computer's data
    ref = db.reference(f'/tasks/{COMPUTER_ID}')
    
    def listener(event):
        print(f'New task added by {COMPUTER_ID}:', event.data)
    
    ref.listen(listener)

import uuid # <------ this is for using the actual computer name

# Dynamic unique identifier based on MAC address
COMPUTER_ID = uuid.UUID(int=uuid.getnode()).hex[-12:]

    

"""

"""
            Firebase commands [Above]

"""

def format_sentence(sentence, words_per_line=20):
    formatted_sentence = []
    for i, word in enumerate(sentence.split()):
        formatted_sentence.append(word)
        if i != 0 and i % words_per_line == 0:
            formatted_sentence.append("\n")
    return " ".join(formatted_sentence)

def delete_last_entry(df):
    if not df.empty:
        df = df[:-1]  # Remove the last row
        df.to_csv(filename, index=False)
        print("Last entry deleted from the CSV file.")
        return df
    else:
        print("CSV file is empty. No entries to delete.")

    return df

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
        return int(duration.total_seconds() / 60)

    return None

def calculate_DCR_duration(df):
    # Check if there is at least one 'begin DCR' entry
    start_DCR_entries = df[df['task'].str.contains('start DCR', na=False, case=False)]
    if not start_DCR_entries.empty:
        
        # Get the timestamp of the last 'start task' entry
        last_DCR_task_time = pd.to_datetime(start_DCR_entries['time'].iloc[-1])

        # Get the current time
        current_time = datetime.now()
        print("Good job")
        # Calculate the duration
        duration = current_time - last_DCR_task_time
        return int(duration.total_seconds() / 60)

    return None

def record_speech():
    r = sr.Recognizer()
    mic = sr.Microphone()
    winsound.Beep(1000, 500)
    with mic as source:
        audio = r.listen(source)
    winsound.Beep(700, 400)
    # recording session info
    current_time = datetime.now().strftime("%H:%M:%S")
    speech = r.recognize_google(audio)

    return speech, current_time

def add_row(df, data):
    df2 = pd.DataFrame(data)
    df = pd.concat([df, df2], ignore_index=True)
    return df

def execute_task(df, speech, current_time):
    speech = format_sentence(speech)
    # Check if the word "delete" is spoken
    
    if speech.lower().startswith("start task"):
        #df = add_row(df, {'time': [current_time], 'task': [speech]})
        print("Task Timer Started")
        winsound.Beep(1200, 400)
    if speech.lower().startswith("start dcr"):
        #df = add_row(df, {'time': [current_time], 'task': [speech]})
        winsound.Beep(5000, 5000)
    

    if speech.lower().startswith("end dcr"):
        print("DCR Time Counter Stopped")
        

        # Calculate the duration and log it
        duration_minutes = calculate_DCR_duration(df)
        if duration_minutes is not None:
            print(f"DCR duration: {duration_minutes} mins")
        df = add_row(df, {'DCR': [duration_minutes], 'time': [current_time], 'task': [speech]})
        
        data_to_push = {'DCR': duration_minutes, 'time': current_time, 'task': speech}
        # Push the dictionary to Firebase
        add_row_firebase(data_to_push)
        winsound.Beep(1200, 400)
    elif speech.lower().startswith("end task"):
        print("Task Time Counter Stopped")
        

        # Calculate the duration and log it
        duration_minutes = calculate_task_duration(df)
        if duration_minutes is not None:
            print(f"Task duration: {duration_minutes} mins")
        df = add_row(df, {'Points': [duration_minutes], 'time': [current_time], 'task': [speech]})

        data_to_push = {'Points': duration_minutes, 'time': current_time, 'task': speech}
        # Push the dictionary to Firebase
        add_row_firebase(data_to_push)

        winsound.Beep(1200, 400)
    else:
        #speech  != 'delete last row'
        df = add_row(df, {'time': [current_time], 'task': [speech]})
        data_to_push = {'time': current_time, 'task': speech}
        # Push the dictionary to Firebase
        add_row_firebase(data_to_push) 
        
    return df

def write_task(df, filename):
    df.to_csv(filename, index=False)

if __name__ == "__main__":
    filename = '2-15-24.csv'
    df = pd.read_csv(filename)
    speech, current_time = record_speech()
    data = execute_task(df, speech, current_time)
    write_task(data, filename)

if speech == 'delete last row':
        df = delete_last_entry(df)
        print("Deletion logic executed.")
        winsound.Beep(250, 800)


print(speech)
print(f"Current Time: {current_time}")


# you'll need this: pip install firebase-admin




"""
Commands:
'start task'
'start DCR'
'end task'
'end DCR'
'delete last row'

**BEEP FEEDBACK**
A different beep, apart for the beeps that let you know when you are recording,  
will play to let you know your command has been accepted

"""