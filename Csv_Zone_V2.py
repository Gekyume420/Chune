import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import speech_recognition as sr
import time
import winsound
from datetime import datetime
from datetime import datetime, timedelta
import pandas as pd
# Path to your Firebase Admin SDK private key
cred = credentials.Certificate('C:/Users/16198/Desktop/FIREBASE/chunelink-firebase-adminsdk-unh7l-267bbbcfac.json')
# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {'databaseURL': 'https://chunelink-default-rtdb.firebaseio.com/'})

# Static unique identifier
 
COMPUTER_ID = "Nick" # Change this to "id_nicks_computer" on Nick's computer
COMPUTER_ID2 = "Jackson" 

filename = '2-21-24.csv'


def add_row_firebase(data):
    # Reference to your Firebase database path
    ref = db.reference(f'/tasks/{COMPUTER_ID2}')
    #ref = db.reference('/tasks')
    # Pushes a new entry onto the database
    ref.push(data)

def execute_task_firebase(df,time_difference, speech, current_time):
    # Your existing logic here
   
    # Instead of adding to a local DataFrame, push to Firebase
    data = {'time': current_time, 'task': speech, 'task time': time_difference}
    # Depending on the condition, you might want to add more to `data`
    add_row_firebase(data)



ref = db.reference(f'/tasks/{COMPUTER_ID}')
ref2 = db.reference(f'/tasks/{COMPUTER_ID2}')


#print(ref)
#print(ref2)
#######################################################################################################################################
#computer_id = "Jackson"

def get_time_difference_from_last_start_task(computer_id):
    todays_date = datetime.now().strftime("%Y-%m-%d")
    
    # Reference to the tasks of the specific computer ID within the database, under today's date
    ref = db.reference(f'/tasks/{todays_date}/{computer_id}')
    
    tasks = ref.get()
    
    if not tasks:
        return "No tasks found."
    
    latest_start_task_time = None
    
    # Get the current date to use for parsing task times
    current_date = datetime.now().date()
    
    for task_id, task_info in tasks.items():
        # Ensure task_info is a dictionary before accessing it
        if isinstance(task_info, dict) and 'start task' in task_info.get('task', '').lower():
            task_time_str = task_info.get('time')
            if task_time_str:
                # Parse the time with the current date
                task_time = datetime.strptime(f"{current_date} {task_time_str}", "%Y-%m-%d %H:%M:%S")
                if latest_start_task_time is None or task_time > latest_start_task_time:
                    latest_start_task_time = task_time

    if latest_start_task_time:
        current_time = datetime.now()
        time_difference = current_time - latest_start_task_time
        return time_difference - timedelta(days=time_difference.days)
    else:
        return "No 'start task' entries found."




############################################################################################################################################
def record_speech():
    r = sr.Recognizer()
    mic = sr.Microphone()
    winsound.Beep(1000, 500)
    print("\n\n [ Recording in progress ] \n\n")
    
    with mic as source:
        audio = r.listen(source)
    winsound.Beep(700, 400)
    current_time = datetime.now().strftime("%H:%M:%S")
    speech = r.recognize_google(audio)
    return speech, current_time



def fetch_data_and_write_to_csv(computer_id1, computer_id2):
    todays_date = datetime.now().strftime("%Y-%m-%d")
    
    # Adjusted reference paths to include today's date
    ref1 = db.reference(f'/tasks/{todays_date}/{computer_id1}')
    ref2 = db.reference(f'/tasks/{todays_date}/{computer_id2}')
    
    # Fetch the data for both computer IDs
    data1 = ref1.get()
    data2 = ref2.get()

    tasks1 = []
    tasks2 = []

    # Process data1 if it's not None and not empty
    if data1 and isinstance(data1, dict):
        for key, value in data1.items():
            if isinstance(value, dict):  # Ensure value is a dictionary
                value['id'] = key  # Add the 'id' key to the dictionary
                tasks1.append(value)
            else:
                print(f"Unexpected data format for {key} in {computer_id1}: {value}")

    # Process data2 similarly
    if data2 and isinstance(data2, dict):
        for key, value in data2.items():
            if isinstance(value, dict):  # Ensure value is a dictionary
                value['id2'] = key  # Add the 'id2' key to the dictionary
                tasks2.append(value)
            else:
                print(f"Unexpected data format for {key} in {computer_id2}: {value}")

    # Convert to DataFrame and handle empty lists
    df1 = pd.DataFrame(tasks1) if tasks1 else pd.DataFrame()
    df2 = pd.DataFrame(tasks2) if tasks2 else pd.DataFrame()

    # Merge the two DataFrames
    df_merged = pd.merge(df1, df2, left_index=True, right_index=True, how='outer', suffixes=('', '2'))

    # Write the merged DataFrame to a CSV file
    df_merged.to_csv(filename, index=False)
    print(f"Data written to '{filename}' successfully.")



# Function to update task and time in the Firebase database
def update_task_in_database(computer_id, task, time, time_difference):
    # Get today's date in the format YYYY-MM-DD
    todays_date = datetime.now().strftime("%Y-%m-%d")
    
    # Reference to the tasks of the specific computer ID within the database, under today's date
    ref = db.reference(f'/tasks/{todays_date}/{computer_id}')
    
    # Convert the timedelta to a string if it's not None
    if isinstance(time_difference, timedelta):
        time_difference_str = str(time_difference)
       # time_difference_str = time_difference.strftime("%Y-%m-%d")
        print('if statement')
         # Create a new task entry
        new_task_ref = ref.push()
        
        # Set the task and time values in the database
        new_task_ref.set({
            'task': task,
            'time': time,
            'task time': time_difference_str  # Use the string representation
        })
    else:
        
        time_difference_str = '0'
        # Create a new task entry
        new_task_ref = ref.push()
        
        # Set the task and time values in the database
        new_task_ref.set({
            'task': task,
            'time': time,
            'task time': time_difference_str  # Use the string representation
        })
 
# First, record a speech and get the current time
speech, current_time = record_speech()

# AWIUFNAIUWPFPAW---------------------------------------------NEXT: YOU NEED TO PUT IN ALL OF THE SPEECH COMMANDS ------------------------------
if speech.lower().startswith("start task"):
    print("Task Timer Started")
    winsound.Beep(1200, 400)
if speech.lower().startswith("start dcr"):
    winsound.Beep(5000, 1000)

if speech.lower().startswith("end task"):
    print("Task Time Counter Stopped")
    time_difference = get_time_difference_from_last_start_task('Jackson')
    # Print only the hours, minutes, and seconds part if it's a timedelta
    if isinstance(time_difference, timedelta):
        print("Time difference from the last 'start task':", time_difference)
    else:
        print(time_difference)




update_task_in_database('Jackson', speech, current_time, 'task time')

# Then, fetch all data including the new entry and write it to the CSV file
fetch_data_and_write_to_csv('Jackson', 'Nick')

print('\n\n', speech, '\n\n')
print(f"Current Time: {current_time}")





















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