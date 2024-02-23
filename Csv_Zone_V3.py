import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import speech_recognition as sr
import time
import winsound
from datetime import datetime, timedelta
import pandas as pd
# Path to your Firebase Admin SDK private key
cred = credentials.Certificate('C:/Users/16198/Desktop/FIREBASE/chunelink-firebase-adminsdk-unh7l-267bbbcfac.json')
# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {'databaseURL': 'https://chunelink-default-rtdb.firebaseio.com/'})

# Static unique identifier
 
COMPUTER_ID = "Nick" # Change this to "id_nicks_computer" on Nick's computer
COMPUTER_ID2 = "Jackson" 
filename = "2-22-FIREBASE.csv"

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
################################################################################################################################################################
#computer_id = "Jackson"
def calculate_time_since_last_start_task(computer_id):
    # Make sure Firebase has been initialized here
    
    todays_date = datetime.now().strftime("%Y-%m-%d")
    ref = db.reference(f'/tasks/{todays_date}/{computer_id}')
    tasks = ref.get()

    if not tasks:
        print(f"No tasks found for {computer_id} on {todays_date}.")
        return None

    # Filtering tasks to find the last 'start task' entry
    start_task_times = []
    for task_id, task_details in tasks.items():
        if 'task' in task_details and 'start task' in task_details['task'].lower():
            task_time_str = task_details.get('time', '')
            try:
                task_time = datetime.strptime(task_time_str, "%H:%M:%S").time()
                start_task_times.append(task_time)
            except ValueError:
                print(f"Invalid time format for task {task_id}")

    if not start_task_times:
        print("No 'start task' entries found.")
        return None

    # Finding the last 'start task' time
    last_start_task_time = max(start_task_times)
    # Current time
    now = datetime.now()
    # Combining the current date with the last start task time for comparison
    last_start_datetime = datetime.combine(now.date(), last_start_task_time)

    # Calculating time difference
    time_difference = now - last_start_datetime
    # Convert time difference to total seconds
    total_seconds = int(time_difference.total_seconds())
    # Convert total seconds to minutes and seconds
    minutes = total_seconds // 60
    #seconds = total_seconds % 60

    # Return or print the time difference in minutes and seconds
    return minutes




################################################################################################################################################################
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
    df_merged.to_csv(filename, index=False)
    print("Data written to 'test_csv.csv' successfully.")


# Function to update task and time in the Firebase database
def update_task_in_database(computer_id, task, time):
    # Get today's date in the format YYYY-MM-DD
    todays_date = datetime.now().strftime("%Y-%m-%d")
    
    # Reference to the tasks of the specific computer ID within the database, under today's date
    ref = db.reference(f'/tasks/{todays_date}/{computer_id}')
    # Create a new task entry
    new_task_ref = ref.push()
  
    # Set the task and time values in the database
    new_task_ref.set({
        'task': task,
        'time': time,
         # Use the string representation
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
if speech.lower().startswith("end task"):
    print("Task Time Counter Stopped")
    computer_id = COMPUTER_ID2  # Use the actual computer_id
    time_diff = calculate_time_since_last_start_task(computer_id)
    if time_diff:
        print(f"Time since last 'start task': {time_diff}")

# Update the task in the Firebase database for the appropriate computer ID
update_task_in_database('Jackson', speech, current_time)

# Then, fetch all data including the new entry and write it to the CSV file
fetch_data_and_write_to_csv('Jackson', 'Nick')

print('\n\n', speech, '\n\n')
print(f"Current Time: {current_time}")




"""
computer_id = COMPUTER_ID2 
todays_date = datetime.now().strftime("%Y-%m-%d")
ref = db.reference(f'/tasks/{todays_date}/{computer_id}')

data = ref.get()
time_values = {}

# Iterate through each task ID and its data
for task_id, task_data in data.items():
    # Extract the 'time' value from each task's data
    if 'time' in task_data:
        time_values[task_id] = task_data['time']


print(f'Time values: {time_values}')

#def get_time_difference_from_last_start_task(computer_id):




"""














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