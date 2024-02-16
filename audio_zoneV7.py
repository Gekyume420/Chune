import speech_recognition as sr
import time
import winsound
from datetime import datetime
import pandas as pd

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
        print("You're being a pussy")
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
        print("GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF GO FUCK YOURSELF ")
        winsound.Beep(5000, 5000)
    

    if speech.lower().startswith("end dcr"):
        print("DCR Time Counter Stopped")
        

        # Calculate the duration and log it
        duration_minutes = calculate_DCR_duration(df)
        if duration_minutes is not None:
            print(f"DCR duration: {duration_minutes} mins")
        df = add_row(df, {'DCR': [duration_minutes], 'time': [current_time], 'task': [speech]})
        #print(df)
        winsound.Beep(1200, 400)
    elif speech.lower().startswith("end task"):
        print("Task Time Counter Stopped")
        

        # Calculate the duration and log it
        duration_minutes = calculate_task_duration(df)
        if duration_minutes is not None:
            print(f"Task duration: {duration_minutes} mins")
        df = add_row(df, {'Points': [duration_minutes], 'time': [current_time], 'task': [speech]})
        #print(df)
        winsound.Beep(1200, 400)
    else:
        #speech  != 'delete last row'
        df = add_row(df, {'time': [current_time], 'task': [speech]}) 
        
    return df



def write_task(df, filename):
    df.to_csv(filename, index=False)

# delete last task entry
# start a task
# end a task


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

if speech.lower().startswith("start dcr"):
    print("\n \nI WILL KILL YOU FAGGOT, STOP BEING A FUCKING PUSSY")
    winsound.Beep(5400, 4000)
    print("\nYOU'RE SUCH A LITTLE BITCH FOR NEEDING YOUR PHONE, FUCK YOU\n")
    winsound.Beep(5500, 4000)
    print("\nTHIS SHIT IS ABOUT TO GET WAY WORSE IF YOU DONT PUT YOUR PANZIE ASS PHONE DOWN\n")
    winsound.Beep(6000, 3000)
    print("\nTHIS IS WHAT YOU DESERVE FOR THINKING YOU 'NEEDED YOUR PHONE'\n")
    winsound.Beep(6200, 4000)
    print("\nGOGGINS MENTALITY, JOCKO WILINK, GARY VEE MINDSET ONLY\n")
    winsound.Beep(6350, 4000)
    print("\n'it's too hard living in a first world country, ohhh just one more video to ease the pain' FUCK YOU\n")
    winsound.Beep(6500, 5000)
    print("\nTAKE A STEP BACK AND LITERALLY FUCK YOUR OWN FACE\n")
    winsound.Beep(6650, 5000)
    print("\nYOU ARE CURRENTLY ABOUT TO MAKE YOUR LIFE TANGIBLY WORSE\n")
    winsound.Beep(6800, 5000)
    print("\n\n\n enjoy your faggot video you piece of shit \n")
print(speech)
print(f"Current Time: {current_time}")



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