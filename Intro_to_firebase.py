computer_id = COMPUTER_ID2 
todays_date = datetime.now().strftime("%Y-%m-%d")
ref = db.reference(f'/tasks/{todays_date}/{computer_id}')
data = ref.get()
time_values = {}
task_description = {}

# Iterate through each task ID and its data
for task_id, task_data in data.items():
    # Extract the 'time' value from each task's data
    if 'time' in task_data:
        time_values[task_id] = task_data['time']

print(f'Time values: {time_values}')

####### brings you all of the time values in the database 
### you don't need "task" in task_id/task_data

# Iterate through each task ID and its data
for task_id, task_data in data.items():
    # Extract the 'time' value from each task's data
    if 'task' in task_data:
        task_description[task_id] = task_data['task']

print(f'Task Description: {task_description}')





###################################

def update_task_in_database(computer_id, task, time, minutes):
    # Get today's date in the format YYYY-MM-DD
    todays_date = datetime.now().strftime("%Y-%m-%d")
    
    # Reference to the tasks of the specific computer ID within the database, under today's date
    ref = db.reference(f'/tasks/{todays_date}/{computer_id}')
    # Create a new task entry
    new_task_ref = ref.push()

    if speech.lower().startswith("end task"):
    # Set the task and time values in the database
        new_task_ref.set({
            'task': task,
            'time': time
            'task time': minutes 
        })
    else:
          new_task_ref.set({
            'task': task,
            'time': time
        })