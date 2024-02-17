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
 
COMPUTER_ID = "Nick" # Change this to "id_nicks_computer" on Nick's computer
COMPUTER_ID2 = "Jackson" 


"""
            Firebase commands [Below]

"""

def add_row_firebase(data):
    # Reference to your Firebase database path
    ref = db.reference(f'/tasks/{COMPUTER_ID2}')
    #ref = db.reference('/tasks')
    # Pushes a new entry onto the database
    ref.push(data)

def execute_task_firebase(df, speech, current_time):
    # Your existing logic here
   
    # Instead of adding to a local DataFrame, push to Firebase
    data = {'time': current_time, 'task': speech}
    # Depending on the condition, you might want to add more to `data`
    add_row_firebase(data)



ref = db.reference(f'/tasks/{COMPUTER_ID}')
ref2 = db.reference(f'/tasks/{COMPUTER_ID2}')


#print(ref)
#print(ref2)
################################
#computer_id = "Jackson"


#################################
def record_speech():
    r = sr.Recognizer()
    mic = sr.Microphone()
    winsound.Beep(1000, 500)
    with mic as source:
        audio = r.listen(source)
    winsound.Beep(700, 400)
    current_time = datetime.now().strftime("%H:%M:%S")
    speech = r.recognize_google(audio)
    return speech, current_time



def fetch_data_and_write_to_csv(computer_id1, computer_id2):
    # Reference to the tasks of the specific computer IDs within the database
    ref1 = db.reference(f'/tasks/{computer_id1}')
    ref2 = db.reference(f'/tasks/{computer_id2}')

    # Fetch the data for both computer IDs
    data1 = ref1.get()
    data2 = ref2.get()

    # Check if data is not None and not empty, for both IDs
    if data1:
        tasks1 = []
        for key, value in data1.items():
            task_info = value
            task_info['id'] = key  # Capture the unique key if you want to preserve it
            tasks1.append(task_info)

        df1 = pd.DataFrame(tasks1)

    else:
        print(f"No data found or the data is empty for {computer_id1}.")
        df1 = pd.DataFrame()

    if data2:
        tasks2 = []
        for key, value in data2.items():
            task_info = value
            task_info['id2'] = key  # Capture the unique key if you want to preserve it
            tasks2.append(task_info)

        df2 = pd.DataFrame(tasks2)

    else:
        print(f"No data found or the data is empty for {computer_id2}.")
        df2 = pd.DataFrame()

    # Merge the two DataFrames based on index (this will align the rows to the same index)
    df_merged = pd.merge(df1, df2, left_index=True, right_index=True, how='outer',
                         suffixes=('', '2'))

    # Write the merged DataFrame to a CSV file
    df_merged.to_csv('test_csv.csv', index=False)
    print("Data written to 'test_csv.csv' successfully.")


# Function to update task and time in the Firebase database
def update_task_in_database(computer_id, task, time):
    # Reference to the tasks of the specific computer ID within the database
    ref = db.reference(f'/tasks/{computer_id}')
    # Create a new task entry
    new_task_ref = ref.push()
    # Set the task and time values in the database
    new_task_ref.set({
        'task': task,
        'time': time
    })

# Function to fetch data and write it to a CSV file, this remains unchanged
#...

# Here's how you would use these functions together:
# First, record a speech and get the current time
speech, current_time = record_speech()

# AWIUFNAIUWPFPAW---------------------------------------------NEXT: YOU NEED TO PUT IN ALL OF THE SPEECH COMMANDS ------------------------------
if speech.lower().startswith("start task"):
    print("Task Timer Started")
    winsound.Beep(1200, 400)
if speech.lower().startswith("start dcr"):
    winsound.Beep(5000, 1000)


# Update the task in the Firebase database for the appropriate computer ID
update_task_in_database('Jackson', speech, current_time)

# Then, fetch all data including the new entry and write it to the CSV file
fetch_data_and_write_to_csv('Jackson', 'Nick')





















"""
#This function will print out new tasks as they're added to the database. You can adapt it to merge new entries into your local CSV file or take any other action needed.
def listen_for_nick_changes():
    # Listen for changes only in the specific computer's data
    ref = db.reference(f'/tasks/{COMPUTER_ID}')
    
    def listener(event):
        print(f'New task added by {COMPUTER_ID}:', event.data)
        process_and_update_csv(event.data)
    ref.listen(listener)

import uuid # <------ this is for using the actual computer name

# Dynamic unique identifier based on MAC address
COMPUTER_ID = uuid.UUID(int=uuid.getnode()).hex[-12:]

"""