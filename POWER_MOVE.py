import firebase_admin 
from firebase_admin import credentials
from firebase_admin import db
import speech_recognition as sr
from datetime import datetime, timedelta
import pandas as pd
import os
import uuid 
from dotenv import load_dotenv



load_dotenv()

database_url = os.environ['DATABASE_URL']
credentials_path = os.environ['CREDENTIALS_PATH']
filename_folder = os.environ['CSV_PATH']
filename2_folder = os.environ['REMINDERS_PATH']
#db = DB(database_url, credentials_path)

"""
        CHANGE YOUR .ENV FILE, JUST ADD SOMETHING LIKE THIS
"""
        #EXAMPLE: CSV_PATH="C:\Users\16198\Documents\PYTHON\Daily Schedules
"""

"""


todays_date = datetime.now().strftime("%Y-%m-%d")
filename = filename_folder + "\Schedule_" + todays_date + ".csv"
filename2 = filename2_folder + "\Reminders_" + todays_date + ".csv"

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
    COMPUTER_ID3 = None
    text = None
    
    if comp_name == 'f21898950b33':
        COMPUTER_ID = 'Nick'
        COMPUTER_ID2 = 'Jackson'
        COMPUTER_ID3 = 'Kai'
        text = COMPUTER_ID + ' is  gay  8====D'
    if comp_name == '2cf05d760155':
        COMPUTER_ID = 'Jackson'
        COMPUTER_ID3 = 'Kai'
        COMPUTER_ID2 = 'Nick'
        text = 'Welcome ,  King'
    else:
        COMPUTER_ID = 'Kai'
        COMPUTER_ID2 = 'Jackson'
        COMPUTER_ID3 = 'Nick'
        #text = 'Welcome ,  King'
    return COMPUTER_ID, COMPUTER_ID2, COMPUTER_ID3, text


COMPUTER_ID, COMPUTER_ID2, COMPUTER_ID3, text = determine_computer_ids()

computer_id1 = COMPUTER_ID

debug_mode = False


if debug_mode == False:

    path1 = (f'/main/{todays_date}/{computer_id1}/log')
    path1s = (f'/main/{todays_date}/{computer_id1}/subtask')
else:
    path1 = (f'/debug/{todays_date}/{computer_id1}/log')
    path1s = (f'/debug/{todays_date}/{computer_id1}/subtask')
#result = pyfiglet.figlet_format(text) 
#print(result) 
#time.sleep(1)


"""
            Grab these paragraph comments so you don't have to keep fucking with them

"""

#ref = db.reference(f'/tasks/{COMPUTER_ID}')


################################################################################################################################################################
""" kinda ran out of steam at exactly this moment, this is a good idea though, you also need to read how CLASSES work

def key_words_sorter(speech, key_words):

    if speech

class ActionHandler:
    def action_a(self):
        print("Executing Function A: Task related action.")

    def action_b(self):
        print("Executing Function B: DCR related action.")

    def action_c(self):
        print("Executing Function C: Adding a reminder.")

    def execute(self, command):
        # Check for task related commands
        if command.startswith('end task') or command.startswith('stop task'):
            self.action_a()
        # Check for DCR related commands
        elif command.startswith('end DCR') or command.startswith('stop DCR'):
            self.action_b()
        # Check for adding a reminder
        elif command.startswith('add reminder'):
            self.action_c()
        else:
            print("Invalid command")

# Example usage
handler = ActionHandler()

for input_str in inputs:
    print(f"Input: {input_str}")
    handler.execute(input_str)
    print("---")

"""

def calculate_time_since_last_start(computer_id1, task_keyword):
    # Make sure Firebase has been initialized here

    todays_date = datetime.now().strftime("%Y-%m-%d")
    ref = db.reference(path1)
    tasks = ref.get()

    if not tasks:
        print(f"No tasks found for {computer_id1} on {todays_date}.")
        return None

    # Filtering tasks to find the last relevant 'start' entry based on task_keyword
    start_task_times = []
    for task_id, task_details in tasks.items():
        if 'task' in task_details and task_keyword in task_details['task'].lower():
            task_time_str = task_details.get('time', '')
            try:
                task_time = datetime.strptime(task_time_str, "%H:%M:%S").time()
                start_task_times.append(task_time)
            except ValueError:
                print(f"Invalid time format for task {task_id}")

    if not start_task_times:
        print(f"No '{task_keyword}' entries found.")
        return None

    # Finding the last relevant 'start' time
    last_start_task_time = max(start_task_times)
    # Current time
    now = datetime.now()
    # Combining the current date with the last start task time for comparison
    last_start_datetime = datetime.combine(now.date(), last_start_task_time)

    # Calculating time difference
    time_difference = now - last_start_datetime
    # Convert time difference to total seconds
    total_seconds = int(time_difference.total_seconds())
    # Convert total seconds to minutes
    minutes = total_seconds // 60

    # Return the time difference in minutes
    return minutes




def decide_and_calculate_minutes(computer_id1, speech):
    # Initialize task_keyword before if-else chain
    task_keyword = None

    # Use if-elif-else structure to ensure only one block executes
    if speech.lower().startswith("stop task") or speech.lower().startswith("end task"):
        task_keyword = 'start task'
        print('stop task logged')
    elif speech.lower().startswith("stop lab") or speech.lower().startswith("end lab"):
        task_keyword = 'start lab'
    elif speech.lower().startswith("stop dcr") or speech.lower().startswith("end dcr"):
        task_keyword = 'start dcr'
    else:
        print("Non-delta t related entry")
        return None, None

    # Calculate minutes if task_keyword was set
    if task_keyword:
        minutes = calculate_time_since_last_start(computer_id1, task_keyword)
        return minutes, task_keyword
    else:
        # This else is not strictly necessary due to the return statement in the first else,
        # but it's here for logical completeness.
        return None, None
################################################################################################################################################################





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



def fetch_data_and_write_to_csv(computer_id1, computer_id2, computer_id3,context):
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
    data1 = db.reference(path1).get()
    data2 = db.reference(f'/main/{todays_date}/{computer_id2}/log').get()
    data3 = db.reference(f'/main/{todays_date}/{computer_id3}/log').get()

    tasks1 = process_data(data1)
    tasks2 = process_data(data2, '2')  # Suffix for id in the second dataframe
    tasks3 = process_data(data3, '3')

    df1 = pd.DataFrame(tasks1)
    df2 = pd.DataFrame(tasks2)
    df3 = pd.DataFrame(tasks3)

    # Calculate total points and DCR times for each DataFrame, considering only non-zero values
    total_points1 = df1['points'].dropna().astype(int).sum() if 'points' in df1.columns else 0
    total_points2 = df2['points'].dropna().astype(int).sum() if 'points' in df2.columns else 0
    total_points3 = df3['points'].dropna().astype(int).sum() if 'points' in df3.columns else 0

    total_dcr1 = df1['DCR time'].dropna().astype(int).sum() if 'DCR time' in df1.columns else 0
    total_dcr2 = df2['DCR time'].dropna().astype(int).sum() if 'DCR time' in df2.columns else 0
    total_dcr3 = df3['DCR time'].dropna().astype(int).sum() if 'DCR time' in df3.columns else 0

    # First, merge df1 and df2
    df_merged = pd.merge(df1, df2, left_index=True, right_index=True, how='outer', suffixes=('', '2'))

    # Then, merge the result with df3
    df_merged = pd.merge(df_merged, df3, left_index=True, right_index=True, how='outer', suffixes=('', '3'))


    # Add a new row for 'Total Points' and 'Total DCR time'
    #df_merged.loc['Total', 'points'] = f"{(total_points1 / 60):.1f}"
    df_merged.loc['Total', 'points'] = total_points1
    df_merged.loc['Total', 'points2'] = total_points2
    df_merged.loc['Total', 'points3'] = total_points3

    df_merged.loc['Total', 'DCR time'] = total_dcr1
    df_merged.loc['Total', 'DCR time2'] = total_dcr2
    df_merged.loc['Total', 'DCR time3'] = total_dcr3



    subtask_data = db.reference(f'/main/{todays_date}/{computer_id1}/subtask').get()
    subtask_total_start_lab = 0

    if subtask_data and isinstance(subtask_data, dict):
        # Sum the 'start lab' values from each subtask
        for key in subtask_data:
            subtask_total_start_lab += int(subtask_data[key].get('start lab', 0))

    # Remove 'idsubtask' column if it exists
    if 'idsubtask' in df_merged.columns:
        df_merged.drop(columns='idsubtask', inplace=True)

    # Add the 'start lab' total to the DataFrame in a new row
    subtask_row = pd.DataFrame({'points': [subtask_total_start_lab]}, index=[context])
    
    # Append the 'Subtask Total' row to the DataFrame
    df_merged = df_merged._append(subtask_row)

    # Write the final DataFrame to a CSV file
    df_merged.to_csv(filename, index_label='Index')
    print("Data written to", filename, "successfully.")

# Instead of 'start lab' being it's own column, I would instead like 'Subtask Total' to be 


"""
    def process_subdata(data, id_suffix=''):
        tasks = []
        if data:
            for key, value in data.items():
                # Include the unique key as 'id'
                value['id' + id_suffix] = key
                # Convert 'points' to an integer if it exists, else NaN
                value[context] = int(value[context]) if {context} in value and value[context] else pd.NA
                
                tasks.append(value)
        return tasks
"""


"""
    df_merged.loc['', 'points'] = ''
    df_merged.loc['Trackable Statistics:', 'points'] = ''
    #df_merged.loc['DCR / Task Time Ratio', 'points'] = f"{(total_dcr1 / total_points1) * 100:.2f}%"
    df_merged.loc['Lab time', 'points'] = '42'
    df_merged.loc['Working on Tandem', 'points'] = '159'
    df_merged.loc['Shits Taken', 'points'] = '3'
"""

    







"""
2 things

1) broadcast a "is_timing_a_task": True that way everytime you make an update you can add to your counter 
2) broadcast the appendix value, this will help you sort the data later
3) figure out how/why the lab is being placed into a column
    the key to solving this might be in the .get() command

4) the data tree might need to be reformatted such that tasks --> todays date --> ComputerID --> task/csv_data --> sub-task(lab time)
5) you will probaably need to move everything from being under computerid to being under 'thought log' / tasks
6) get rid of tasks at the start

7) 

"""







# Function to update task and time in the Firebase database
def update_task_in_database(computer_id1, task, time, context, minutes=None, task_minutes=None, DCR_minutes=None):
    """
    Updates the task in the database with the given computer_id, task, and time.
    Optionally includes minutes or DCR_minutes if provided.
    
    Args:
    - computer_id (str): The computer ID to update the task for.
    - task (str): The task to be updated.
    - time (str): The time at which the task is updated.
    - minutes (int, optional): The task time in minutes, for task time updates.
    - DCR_minutes (int, optional): The DCR time in minutes, for DCR time updates.
    """

    todays_date = datetime.now().strftime("%Y-%m-%d")
    ref = db.reference(path1)
    new_task_ref = ref.push()

    task_data = {
        'task': task,
        'time': time
    }
    
    # Conditionally add points or DCR time to the task data
    if task_minutes is not None:
        task_data['points'] = task_minutes
    if DCR_minutes is not None:
        task_data['DCR time'] = DCR_minutes
    if context is not None:
        print('there is context')
        ref = db.reference(f'/main/{todays_date}/{computer_id1}/subtask')
        sub_task_ref = ref.push()
        subtask_data = {context: minutes}
        sub_task_ref.set(subtask_data)
    # Set the task data in the database
    new_task_ref.set(task_data)



# First, record a speech and get the current time
speech, current_time = record_speech()
#update_task_in_database(COMPUTER_ID, speech, current_time, task_minutes, DCR_minutes):
minutes, context = decide_and_calculate_minutes(COMPUTER_ID, speech)
################################################################################################################################################################
def add_row(df, data):
    df2 = pd.DataFrame(data)
    df = pd.concat([df, df2], ignore_index=True)
    return df

def write_task(df, filename):
    df.to_csv(filename, index=False)
def add_reminder(df, speech, current_time):
    global filename2
    if speech.lower().startswith("add reminder"):
        speech = speech.split(' ', 2)[2]
        df = add_row(df, {'time': [current_time], 'Reminder': [speech]}) 
        
        print("Reminder added")
    
    return df



# Example DataFrame

# Check if the file exists
if not os.path.isfile(filename2):
    df = pd.DataFrame()
    # Save the DataFrame to CSV if the file does not exist
    df.to_csv(filename2)
else:
    print(f"The file {filename2} already exists.")
    todays_date = datetime.now().strftime("%Y-%m-%d")
    df = pd.read_csv(filename2)                             #<----------- it's this, it's not reading the csv because there is no csv
                                                        # that's why it worked yesterday, because it didn't read until after it was created 

    data = add_reminder(df, speech, current_time)
    write_task(data, filename2)

"""
if not os.path.exists(filename2):
    
    df = pd.DataFrame({'Column1': [1, 2], 'Column2': [3, 4]})
    data = add_reminder(df, speech, current_time)
    write_task(data, filename2)

todays_date = datetime.now().strftime("%Y-%m-%d")
df = pd.read_csv(filename2)                             #<----------- it's this, it's not reading the csv because there is no csv
                                                    # that's why it worked yesterday, because it didn't read until after it was created 

data = add_reminder(df, speech, current_time)
write_task(data, filename2)

"""

################################################################################################################################################################


# Depending on the context, update the database accordingly
if context == 'start task':
    update_task_in_database(COMPUTER_ID, speech, current_time, context, task_minutes=minutes)
elif context == 'start dcr':
    update_task_in_database(COMPUTER_ID, speech, current_time, context, DCR_minutes=minutes)
else:
    update_task_in_database(COMPUTER_ID, speech, current_time, context, minutes)



# Then, fetch all data including the new entry and write it to the CSV file
fetch_data_and_write_to_csv(COMPUTER_ID, COMPUTER_ID2, COMPUTER_ID3, context)

print('\n\n', speech, '\n\n')
print(f"Current Time: {current_time}")





