import firebase_admin 
from firebase_admin import credentials
from firebase_admin import db
import speech_recognition as sr
from datetime import datetime, timedelta
import pandas as pd
import os
import uuid 
from dotenv import load_dotenv
import time
import pyfiglet
from quo import echo


load_dotenv()

database_url = os.environ['DATABASE_URL']
credentials_path = os.environ['CREDENTIALS_PATH']
filename_folder = os.environ['CSV_PATH']
#db = DB(database_url, credentials_path)

"""
        CHANGE YOUR .ENV FILE, JUST ADD SOMETHING LIKE THIS
"""
        #EXAMPLE: CSV_PATH="C:\Users\16198\Documents\PYTHON\Daily Schedules
"""

"""


todays_date = datetime.now().strftime("%Y-%m-%d")
filename = filename_folder + "\Schedule_" + todays_date + ".csv"

# Path to your Firebase Admin SDK private key
cred = credentials.Certificate(credentials_path)
firebase_admin.initialize_app(cred, {'databaseURL': database_url})


# fix for mac
try:
    import winsound
except:
    pass

def determine_computer_ids():
    
    comp_name = uuid.UUID(int=uuid.getnode()).hex[-12:]
    
    COMPUTER_ID = None
    COMPUTER_ID2 = None
    text = None
    
    if comp_name == 'f21898950b33':
        COMPUTER_ID = 'Nick'
        COMPUTER_ID2 = 'Jackson'
        text = COMPUTER_ID + ' is  gay  8====D'
    elif comp_name == '2cf05d760155':
        COMPUTER_ID = 'Jackson'
        COMPUTER_ID2 = 'Nick'
        text = 'Welcome ,  King'
    return COMPUTER_ID, COMPUTER_ID2, text


COMPUTER_ID, COMPUTER_ID2, text = determine_computer_ids()

result = pyfiglet.figlet_format(text) 
print(result) 
#time.sleep(1)


"""
            Grab these paragraph comments so you don't have to keep fucking with them

"""

ref = db.reference(f'/tasks/{COMPUTER_ID}')


################################################################################################################################################################

def calculate_time_since_last_start_task(computer_id):
    
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

def calculate_time_since_last_start_DCR(computer_id):
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
        if 'task' in task_details and 'start dcr' in task_details['task'].lower():
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
    DCR_minutes = total_seconds // 60
    #seconds = total_seconds % 60

    # Return or print the time difference in minutes and seconds
    return DCR_minutes



################################################################################################################################################################
def record_speech():
    r = sr.Recognizer()
    mic = sr.Microphone()
    if os.name == 'nt':
        winsound.Beep(1000, 500)
    print("\n\n [ Recording in progress ] \n\n")
    
    with mic as source:
        audio = r.listen(source)
    
    if os.name == 'nt':
        winsound.Beep(700, 400)
    current_time = datetime.now().strftime("%H:%M:%S")
    speech = r.recognize_google(audio)
    return speech, current_time



def fetch_data_and_write_to_csv(computer_id1, computer_id2):
    todays_date = datetime.now().strftime("%Y-%m-%d")
    global filename  # Use the globally defined filename

    # Function to process tasks, points, and DCR times
    def process_data(data, id_suffix=''):
        tasks = []
        if data:
            for key, value in data.items():
                # Include the unique key as 'id'
                value['id' + id_suffix] = key
                # Convert 'points' to an integer if it exists, else NaN
                value['points'] = int(value['points']) if 'points' in value and value['points'] else pd.NA
                # Convert 'DCR time' to an integer if it exists, else NaN
                value['DCR time'] = int(value['DCR time']) if 'DCR time' in value and value['DCR time'] else pd.NA
                tasks.append(value)
        return tasks

    # Fetch the data for both computer IDs
    data1 = db.reference(f'/tasks/{todays_date}/{computer_id1}').get()
    data2 = db.reference(f'/tasks/{todays_date}/{computer_id2}').get()

    tasks1 = process_data(data1)
    tasks2 = process_data(data2, '2')  # Suffix for id in the second dataframe

    df1 = pd.DataFrame(tasks1)
    df2 = pd.DataFrame(tasks2)

    # Calculate total points and DCR times for each DataFrame, considering only non-zero values
    total_points1 = df1['points'].dropna().astype(int).sum() if 'points' in df1.columns else 0
    total_points2 = df2['points'].dropna().astype(int).sum() if 'points' in df2.columns else 0
    total_dcr1 = df1['DCR time'].dropna().astype(int).sum() if 'DCR time' in df1.columns else 0
    total_dcr2 = df2['DCR time'].dropna().astype(int).sum() if 'DCR time' in df2.columns else 0

    # Merge the two DataFrames based on index (this will align the rows to the same index)
    df_merged = pd.merge(df1, df2, left_index=True, right_index=True, how='outer', suffixes=('', '2'))

    # Add a new row for 'Total Points' and 'Total DCR time'
    df_merged.loc['Total', 'points'] = total_points1
    df_merged.loc['Total', 'points2'] = total_points2
    df_merged.loc['Total', 'DCR time'] = total_dcr1
    df_merged.loc['Total', 'DCR time2'] = total_dcr2

    # Write the final DataFrame to a CSV file
    df_merged.to_csv(filename, index_label='Index')
    print("Data written to", filename, "successfully.")


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

def execute_task_firebase_task_time(computer_id, task, time,minutes):
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
        'points': minutes
         # Use the string representation
    })
def execute_task_firebase_DCR_time(computer_id, task, time,DCR_minutes):
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
        'DCR time': DCR_minutes
         # Use the string representation
    })

# First, record a speech and get the current time
speech, current_time = record_speech()

# AWIUFNAIUWPFPAW---------------------------------------------NEXT: YOU NEED TO PUT IN ALL OF THE SPEECH COMMANDS ------------------------------
if speech.lower().startswith("start task"):
    print("Task Timer Started")
    if os.name == 'nt':
        winsound.Beep(1200, 400)
if speech.lower().startswith("start dcr"):
    if os.name == 'nt':
        winsound.Beep(5000, 100)
if speech.lower().startswith("stop task") or speech.lower().startswith("end task"):
    print("Task Time Counter Stopped")
    time_diff = calculate_time_since_last_start_task(COMPUTER_ID)
    execute_task_firebase_task_time(COMPUTER_ID, speech, current_time,time_diff)
    if time_diff:
        print(f"Time since last 'start task': {time_diff}")
    
if speech.lower().startswith("stop dcr") or speech.lower().startswith("end dcr"):
    print("Task Time Counter Stopped")

    time_diff = calculate_time_since_last_start_DCR(COMPUTER_ID)
    execute_task_firebase_DCR_time(COMPUTER_ID, speech, current_time,time_diff)
    if time_diff:
        print(f"Time since last 'start DCR': {time_diff}")
    

if  speech.lower != speech.lower().startswith("stop tasks"):
        update_task_in_database(COMPUTER_ID, speech, current_time)



# Then, fetch all data including the new entry and write it to the CSV file
fetch_data_and_write_to_csv(COMPUTER_ID, COMPUTER_ID2)

print('\n\n', speech, '\n\n')
print(f"Current Time: {current_time}")





