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

todays_date = datetime.now().strftime("%Y-%m-%d")

load_dotenv()

#could also create a 1 time questionaire that you put the info into
database_url = os.environ['DATABASE_URL']
credentials_path = os.environ['CREDENTIALS_PATH']
#filename_folder = os.environ['CSV_PATH']
filename2_folder = os.environ['REMINDERS_PATH']
user_name = os.environ['USER_NAME']
#db = DB(database_url, credentials_path)



filename2 = filename2_folder + "\Reminders_" + todays_date + ".csv"

# Path to your Firebase Admin SDK private key
cred = credentials.Certificate(credentials_path)
firebase_admin.initialize_app(cred, {'databaseURL': database_url})

# fix for mac
try:
    import winsound
except:
    pass

path1 = ''

def debug():
    global path1
    debug_mode = debug_var.get() == 1  # 1 if checked (True), 0 if unchecked (False)

    name = name_var.get()
    if not debug_mode:
        
        path1 = (f'/main/{name}/{todays_date}/log')

    else :
        path1 = (f'/debug/{name}/{todays_date}/log')
        
    return path1

#result = pyfiglet.figlet_format(text) 
#print(result) 
#time.sleep(1)


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
    
    if tag is not None:
        task_data[tag] = task_minutes
    if task_minutes is not None:
        task_data['points'] = task_minutes
    if DCR_minutes is not None:
        task_data['DCR time'] = DCR_minutes
    
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
    print(f"\n{speech}\n\nReminder added")
    
    return df

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

###########################################################################################################################################################
def main():
    
    debug()
    
    tag = tag_var.get()
    name = name_var.get()
    
    
    speech, current_time = record_speech()
    
    minutes, context = decide_and_calculate_minutes(name, speech)
    if context == 'start task':
        update_task_in_database(tag, speech, current_time, context, task_minutes=minutes)
    elif context == 'start dcr':
        update_task_in_database(tag, speech, current_time, context, DCR_minutes=minutes)
    else:
        update_task_in_database(tag, speech, current_time, context, minutes)

    #update_category_sums()
    update_gui_with_user_sums(usernames)
    fetch_tasks_and_times(user_name, format_date(current_date))

    print('\n\n', speech, '\n\n')
    print(f"Current Time: {current_time}")

################################################################################################################################################################
root = tk.Tk()
root.title("Tandem 1.0.1 -alpha")
color_var = tk.IntVar()


"""
UN-COMMENT THIS BULLSHIT TO HELP W/ THE GUI LAYOUT (hint: if "columnspan=3" is said too many times it fucks up everything)


# Create a grid of Frame widgets with distinct background colors
for r in range(16):  # Adjust the range based on your grid
    for c in range(3):  # Adjust the range based on your grid
        frame = tk.Frame(root, borderwidth=1, relief="solid", bg="grey")
        frame.grid(row=r, column=c, padx=5, pady=5, sticky="nsew")

# Now, you can create your actual widgets and place them on top of the grid frames

# Configure the column and row weights to ensure that they expand equally
for i in range(16):  # Adjust the range based on your grid
    root.grid_columnconfigure(i, weight=1)
    root.grid_rowconfigure(i, weight=1)

# Create scrolled text area for displaying the speech
text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD)
text_area.grid(row=0, column=0, columnspan=3, pady=10)  # Spanning across three columns

"""

def create_date_navigator(root):
    current_date = datetime.now()

    def format_date(date):
        return date.strftime("%Y-%m-%d")

    def update_label():
        date_label.config(text=format_date(current_date))

    def decrement_date():
        nonlocal current_date
        current_date -= timedelta(days=1)
        update_label()
       # update_gui_with_user_sums(usernames) #< -- added in post, I think this is how you go about implementing it, just need to modify update_gui_with_user_sums
        fetch_tasks_and_times(name_var.get(),format_date(current_date))  # Refresh tasks based on new date

    def increment_date():
        nonlocal current_date
        current_date += timedelta(days=1)
        update_label()
        fetch_tasks_and_times(name_var.get(),format_date(current_date))  # Refresh tasks based on new date

    # GUI Elements
    left_arrow_button = ttk.Button(root, text="<", command=decrement_date)
    left_arrow_button.grid(row=3, column=0, pady=5, sticky='w')

    date_label = ttk.Label(root, text=format_date(current_date))
    date_label.grid(row=3, column=1, pady=5)

    right_arrow_button = ttk.Button(root, text=">", command=increment_date)
    right_arrow_button.grid(row=3, column=2, pady=5, sticky='e')

    return current_date, format_date

current_date, format_date = create_date_navigator(root)

# Dropdown menu options
options = ['Lab', 'Gym', 'Work', 'Class', 'Tandem', 'Chores', 'None']
tag_var = tk.StringVar()
dropdown = ttk.Combobox(root, textvariable=tag_var, values=options)
dropdown.grid(row=1, column=0, columnspan=3, pady=5)  # Spanning across three columns
dropdown.set('Select a tag')

# future reference names = [{user_name}, 'Nick', 'Kai']
names = ['Jackson', 'Nick', 'Kai']
name_var = tk.StringVar()
dropdown_name = ttk.Combobox(root, textvariable=name_var, values=names)
dropdown_name.grid(row=1, column=0, pady=5)
dropdown_name.set(user_name)
# Create a button to start recording
record_btn = tk.Button(root, text="Record Speech", command=main)
record_btn.grid(row=2, column=0, pady=5, sticky='ew')  # Aligned in the first column

# Create the debug mode checkbox
debug_var = tk.IntVar()
debug_checkbox = tk.Checkbutton(root, text="Debug Mode", variable=debug_var, command=debug)
debug_checkbox.grid(row=2, column=1, pady=5)  # Aligned in the second column

debug()
########################################################--------------------------------------------------------
def calculate_sum_for_category(user_name, category, date):
    path = f'/main/{user_name}/{date}/log'  # Dynamic path based on user_name
    ref = db.reference(path)
    category_values = ref.get()

    if not isinstance(category_values, dict):
        # print(f"Data under '{path}' is not in the expected format or is missing. -calculate_sum_for_category") #<-- turn on for debugging
        return 0

    total_sum = 0
    for key, value in category_values.items():
        if isinstance(value, dict) and category in value:
            total_sum += value[category]
    return total_sum

# Create a dictionary to hold the IntVars for each category
category_sums = {category: tk.IntVar(value=0) for category in options}

total_of_totals_var = tk.IntVar(value=0)
# Function to update all category sums & provides the 'Total:' aka total_of_totals


# Create a button to add a reminder
reminder_btn = tk.Button(root, text="Add Reminder", command=add_reminder_button)
reminder_btn.grid(row=2, column=2, pady=5, sticky='ew')  # Aligned in the third column

##########################################$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
def fetch_usernames(exclude_name):
    ref = db.reference('/main')
    all_users = ref.get()  # Fetch all user data under '/main'
    if not all_users:
        return []

    # Filter out the current user and return the list of other usernames
    #usernames = [user for user in all_users if user != exclude_name]
    usernames = [user for user in all_users]
    return usernames

def update_usernames_dropdown(exclude_name):
    usernames = fetch_usernames(exclude_name)
    dropdown_name['values'] = usernames  # Update the dropdown list
    return usernames  # Return the list of usernames
# Call this function with the current username to update the dropdown
# For example, if the current user is 'Jackson', call it like this:


def update_gui_with_user_sums(usernames):
    base_column = 3  # Starting column for the first additional user
    for user_index, user_name in enumerate(usernames):
        user_column = base_column + user_index
        tk.Label(root, text=user_name).grid(row=4, column=user_column)  # User name label
        
        total_of_user_totals = 0
        for i, category in enumerate(options):
            sum_for_category = calculate_sum_for_category(user_name, category, format_date(current_date))
            tk.Label(root, text=f"{category}: {sum_for_category}").grid(row=i+5, column=user_column)
            total_of_user_totals += sum_for_category
        
        # Display total for each user
        tk.Label(root, text=f"Total: {total_of_user_totals}").grid(row=len(options)+6, column=user_column)

# Assuming 'usernames' is already defined or fetched
usernames = update_usernames_dropdown(user_name)
update_gui_with_user_sums(usernames)

##########################################$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$====================================================================================================

def fetch_tasks_and_times(user_name, date):
    
    path = (f"/main/{user_name}/{date}/log") # why does user_name pull up my actual username and not 'Jackson' ?
    ref = db.reference(path)
    tasks = ref.get()

    if not isinstance(tasks, dict):
        print(f"Data under '{path}' is not in the expected format or is missing. -fetch_tasks_and_times")
        text_area.delete(1.0, tk.END)
        text_area.insert(tk.END, "DATA MISSING")
        return

    # Clear the current content in the text area
    text_area.delete(1.0, tk.END)
    
    # Iterate over the tasks and insert them into the text area
    for task_id, task_info in tasks.items():
        if 'task' in task_info and 'time' in task_info:
            text_area.insert(tk.END, f"{task_info['time']} - {task_info['task']}\n")

text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD)
text_area.grid(row=0, column=0, columnspan=3, pady=10, padx=10)

fetch_tasks_and_times(user_name, format_date(current_date)) # starts the script off by loading your personal shit first

 


##########################################$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$====================================================================================================

# Configure the column weights to ensure that they expand equally
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)
#root.grid_columnconfigure(3, weight=1) #this might fuck things up

# Run the Tkinter event loop
root.mainloop()

################################################################################################################################################################

"""
**** Goal for today ****

GLOBAL LAB TIME
Get the point breakdown to display for each user (should I?) -- at least create a method of refering to 
each users total. Use your laptop if you have to.
Honestly may be easier to just say 'NAME = 'JACKSON' ' in the .env file


** put the df in the scrolling text, i.e. have it pull up every entry made before removing the csv portions of code

1) create the total point display in the GUI
    -How would a running total work?

    -For now forget the running total, just put the points into the GUI
    -First metric: display "Global total time spent on lab"

1a) pop up window after "end task", [Please set the task catagory: Work, Gym, School, other]
1b) other gets sent to a different place that I can monitor and begin to include in the code

1c) ! I know you hate the pandas, but it might legitimately be the best way to represent the data in the GUI
1d) create a time travel feature, also add a refresh button that allows you to see the points without calculating the points


% 2) get 'Nick mode' to work
3) get the jackson column to represent all of the data in the database
4) create the kai and nick columns in the GUI
5) points x 1 , tag x .1(or whatever the multiplier is)


I also just thought of this: under each username you could build a path called 'Profile', the cron job puts the data 
into this 


"""


"""
2 things

1) broadcast a "is_timing_a_task": True that way everytime you make an update you can add to your counter 
2) broadcast the appendix value, this will help you sort the data later

"""





"""
You may want to make this feature in another file first and then test it out


current_date = datetime.now()

# Function to update the displayed tasks based on the current_date
def update_displayed_tasks():
    formatted_date = current_date.strftime("%Y-%m-%d")  # Format the date as needed
    # Fetch tasks for `formatted_date` and update the text area
    # ...
    return formatted_date

# Function to move the current date forward
def move_date_forward():
    global current_date
    current_date += timedelta(days=1)  # Move the date forward by one day
    update_displayed_tasks()  # Refresh the displayed tasks

# Function to move the current date backward
def move_date_backward():
    global current_date
    current_date -= timedelta(days=1)  # Move the date back by one day
    update_displayed_tasks()  # Refresh the displayed tasks

# Button to move the date backward
prev_date_btn = tk.Button(root, text="<< Previous Day", command=move_date_backward)
prev_date_btn.grid(row=len(options)+7, column=0, pady=5)

# Button to move the date forward
next_date_btn = tk.Button(root, text="Next Day >>", command=move_date_forward)
next_date_btn.grid(row=len(options)+7, column=2, pady=5)


def fetch_tasks_and_times():
    formatted_date = current_date.strftime("%Y%m%d")
    path = f"/main/Jackson/{formatted_date}/log"
    ref = db.reference(path)
    tasks = ref.get()

    if not isinstance(tasks, dict):
        print(f"Data under '{path}' is not in the expected format or is missing.")
        return

    # Clear the current content in the text area
    text_area.delete(1.0, tk.END)
    
    # Iterate over the tasks and insert them into the text area
    for task_id, task_info in tasks.items():
        if 'task' in task_info and 'time' in task_info:
            text_area.insert(tk.END, f"{task_info['time']} - {task_info['task']}\n")


formatted_date = update_displayed_tasks() # added in post

date_label = tk.Label(root, text=formatted_date)
date_label.grid(row=len(options)+7, column=1, pady=5)
"""