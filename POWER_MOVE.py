import firebase_admin 
from firebase_admin import credentials
from firebase_admin import db
import speech_recognition as sr
from datetime import datetime, timedelta
import pandas as pd
import os
import uuid 
from dotenv import load_dotenv
import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext


################################################################################################################################################################


################################################################################################################################################################



todays_date = datetime.now().strftime("%Y-%m-%d")
todays_month = datetime.now().strftime("%m")
todays_year = datetime.now().strftime("%Y")



"""
todays_date1 = datetime.now()
yesterdays_date = todays_date1 - timedelta(days=1)
todays_date = yesterdays_date.strftime("%Y-%m-%d") # time travel mode
"""


load_dotenv()

database_url = os.environ['DATABASE_URL']
credentials_path = os.environ['CREDENTIALS_PATH']
filename_folder = os.environ['CSV_PATH']
filename2_folder = os.environ['REMINDERS_PATH']
#db = DB(database_url, credentials_path)


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
"""
COMPUTER_ID = ''
COMPUTER_ID2 = ''
"""
computer_id1 = COMPUTER_ID

path1 = ''
path1s = ''

def debug():
    global path1, path1s
    debug_mode = debug_var.get() == 1  # 1 if checked (True), 0 if unchecked (False)
    todays_date = datetime.now().strftime("%Y-%m-%d")
    todays_year = datetime.now().strftime("%Y")
    todays_month = datetime.now().strftime("%m")
    computer_id1 = COMPUTER_ID  # Replace with the actual ID or variable

    if not debug_mode:
        path1 = (f'/main/{todays_year}/{todays_month}/{todays_date}/{computer_id1}/log')
        path1s = (f'/main/{todays_year}/{todays_month}/{todays_date}/{computer_id1}/subtask')
    else:
        path1 = (f'/debug/{todays_year}/{todays_month}/{todays_date}/{computer_id1}/log')
        path1s = (f'/debug/{todays_year}/{todays_month}/{todays_date}/{computer_id1}/subtask')

    return path1, path1s
"""
def switch_user():
    

    nick_mode = nick_var.get() == 1
    if not nick_mode:
        path1 = (f'/main/{todays_year}/{todays_month}/{todays_date}/Nick/log')
        path1s = (f'/main/{todays_year}/{todays_month}/{todays_date}/Nick/subtask')

    

    return path1, path1s
"""
#result = pyfiglet.figlet_format(text) 
#print(result) 
#time.sleep(1)


"""
            Grab these paragraph comments so you don't have to keep fucking with them

"""
################################################################################################################################################################


def calculate_time_since_last_start(computer_id1, task_keyword):
    # Make sure Firebase has been initialized here

    
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
    try:
        speech = r.recognize_google(audio)
    except sr.UnknownValueError:
        print("[Could not understand audio]\n")
    except sr.RequestError as e:
        print("[Could not understand audio]")

    # Check if the checkbox is checked for red text
    if color_var.get() == 1:
        text_color = "red"
    else:
        text_color = "black"
    
    # Configure and insert text with specific color
    text_area.tag_configure("color", foreground=text_color)
    text_area.insert(tk.END, f"{current_time} - {speech}\n", "color")
    text_area.see(tk.END)
    return speech, current_time

    


def fetch_data_and_write_to_csv(computer_id1, computer_id2, computer_id3,context):
    
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

    # Your existing code to fetch and process the main data...

    # Initialize totals for each tag
    tag_totals = {'Gym': 0, 'Class': 0, 'Work': 0, 'Lab': 0, 'Tandem': 0, 'Chores': 0}

    # Fetch all log entries
    log_entries = db.reference(path1).get()

    # Sum the values for each tag
    for entry in log_entries.values():
        for tag in tag_totals:
            if tag in entry:
                tag_totals[tag] += int(entry[tag])

    # Remove 'idsubtask' column if it exists
    if 'idsubtask' in df_merged.columns:
        df_merged.drop(columns='idsubtask', inplace=True)

    # Create a DataFrame for tag totals
    tag_totals_df = pd.DataFrame(list(tag_totals.items()), columns=['task', 'points'])

    # Append the tag totals DataFrame at the end of the merged DataFrame
    final_df = pd.concat([df_merged, tag_totals_df], ignore_index=True)

    # Write the final DataFrame to a CSV file
    final_df.to_csv(filename, index_label='Index')
    print("Data written to", filename, "successfully.")

"""
2 things

1) broadcast a "is_timing_a_task": True that way everytime you make an update you can add to your counter 
2) broadcast the appendix value, this will help you sort the data later

"""
# Function to update task and time in the Firebase database
def update_task_in_database(tag, task, time, context, minutes=None, task_minutes=None, DCR_minutes=None):
    """
    Updates the task in the database with the given computer_id, task, and time.
    Optionally includes minutes or DCR_minutes if provided.
    
    Args:
    - computer_id (str): The computer ID to update the task for.
    - task (str): The task to be updated.
    - time (str): The time at which the task is updated.
    - minutes (int, optional): The task time in minutes, for task time updates.
    - DCR_minutes (int, optional): The DCR time in minutes, for DCR time updates.
    - tag : from the dropdown menu in the GUI
    """

    
    ref = db.reference(path1)
    new_task_ref = ref.push()

    task_data = {
        'task': task,
        'time': time
    }
    
    # i'm not sure how this is working, if should be elif instead of all if commands
    # Conditionally add points or DCR time to the task data

    # need to move "if tag is not None:" part to be under "if task_minutes is not None:" so that it only tags
    # if minutes are being recorded
    if tag is not None:
        task_data[tag] = task_minutes
    if task_minutes is not None:
        task_data['points'] = task_minutes
    if DCR_minutes is not None:
        task_data['DCR time'] = DCR_minutes
    if context is not None:
        print('there is context')
        ref = db.reference(path1s)
        sub_task_ref = ref.push()
        subtask_data = {context: minutes}
        sub_task_ref.set(subtask_data)
    # Set the task data in the database
    new_task_ref.set(task_data)

################################################################################################################################################################
def add_row(df, data):
    df2 = pd.DataFrame(data)
    df = pd.concat([df, df2], ignore_index=True)
    return df

def write_task(df, filename):
    df.to_csv(filename, index=False)
def add_reminder(df, speech, current_time):
    global filename2
    df = add_row(df, {'time': [current_time], 'Reminder': [speech]}) 
    print("Reminder added")
    
    return df
#######################################################################################


def add_reminder_button():
    speech, current_time = record_speech()
    if not os.path.isfile(filename2):
        df = pd.DataFrame()
        # Save the DataFrame to CSV if the file does not exist
        df.to_csv(filename2)
    else:
        print(f"The file {filename2} already exists.")
        
        df = pd.read_csv(filename2) 
    data = add_reminder(df, speech, current_time)
    write_task(data, filename2)

################################################################################################################################################################
"""
Make an "all commands" function?

"""
def main():
    
    debug()
    #switch_user()
    tag = tag_var.get()
    COMPUTER_ID, COMPUTER_ID2, COMPUTER_ID3, text = determine_computer_ids()
    computer_id1 = COMPUTER_ID
    speech, current_time = record_speech()
    
    minutes, context = decide_and_calculate_minutes(COMPUTER_ID, speech)
    if context == 'start task':
        update_task_in_database(tag, speech, current_time, context, task_minutes=minutes)
    elif context == 'start dcr':
        update_task_in_database(tag, speech, current_time, context, DCR_minutes=minutes)
    else:
        update_task_in_database(tag, speech, current_time, context, minutes)

    fetch_data_and_write_to_csv(COMPUTER_ID, COMPUTER_ID2, COMPUTER_ID3, context)

    print('\n\n', speech, '\n\n')
    print(f"Current Time: {current_time}")

################################################################################################################################################################
root = tk.Tk()
root.title("Tandem 1.0.0 -alpha")
color_var = tk.IntVar()

# Create scrolled text area for displaying the speech
text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD)
text_area.grid(row=0, column=0, columnspan=3, pady=10)  # Spanning across three columns

# Dropdown menu options
options = ['Lab', 'Gym', 'Work', 'Class', 'Tandem', 'Chores', 'None']
tag_var = tk.StringVar()
dropdown = ttk.Combobox(root, textvariable=tag_var, values=options)
dropdown.grid(row=1, column=0, columnspan=3, pady=5)  # Spanning across three columns
dropdown.set('Select a tag')

# Create a button to start recording
record_btn = tk.Button(root, text="Record Speech", command=main)
record_btn.grid(row=2, column=0, pady=5, sticky='ew')  # Aligned in the first column

# Create the debug mode checkbox
debug_var = tk.IntVar()
debug_checkbox = tk.Checkbutton(root, text="Debug Mode", variable=debug_var, command=debug)
debug_checkbox.grid(row=2, column=1, pady=5)  # Aligned in the second column

# Create a button to add a reminder
reminder_btn = tk.Button(root, text="Add Reminder", command=add_reminder_button)
reminder_btn.grid(row=2, column=2, pady=5, sticky='ew')  # Aligned in the third column

# Configure the column weights to ensure that they expand equally
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)




"""
nick_var = tk.IntVar()

nick_checkbox = tk.Checkbutton(root, text="Nick Mode", variable=nick_var, command=switch_user)
nick_checkbox.pack()
"""
# Run the Tkinter event loop
root.mainloop()





################################################################################################################################################################

"""

1) create the total point display in the GUI
    -How would a running total work?

    -For now forget the running total, just put the points into the GUI


2) get 'Nick mode' to work
3) get the jackson column to represent all of the data in the database
4) create the kai and nick columns in the GUI

"""






