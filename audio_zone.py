import speech_recognition as sr
import time
import winsound
from datetime import datetime
import openpyxl
import pandas as pd

r = sr.Recognizer()

filename = '2-11-24.csv'

df = pd.read_csv(filename)
# This is just an example; do not run
mic = sr.Microphone()
# Wait for 0.5 seconds
#time.sleep(.5)

# Play a beep sound
  # Beep at 1000 Hz for 500 milliseconds (0.5 seconds)
"""
with mic as source:
    r.adjust_for_ambient_noise(source, duration=1)
"""
winsound.Beep(1000, 500)

with mic as source:
    audio = r.listen(source)

winsound.Beep(700, 400)
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
speech = r.recognize_google(audio)



first_of_data = ""

# Check if the length of speech is greater than X characters (replace X with your desired value)
if len(speech) > 100:  # Change 10 to your desired number of characters
    first_of_data = speech[:100]  # This will store the rest of the data starting from the 11th character
    print(f"First of the data: {first_of_data}")
 
    rest_of_data = speech[100:]
    print(f"Rest of the data: {rest_of_data}")
    # Append new data to the DataFrame
    new_data = {'Timestamp': [current_time], 'Python': [first_of_data]}
    df_new = pd.DataFrame(new_data)
    #Writing to csv
    # Concatenate the new DataFrame with the existing DataFrame, starting at row 2
    #df = pd.concat([df.head(1), df.tail(len(df)-1), df_new], ignore_index=True)
    df = pd.concat([df, df_new], ignore_index=True)
    # Write the updated DataFrame back to the CSV file
    df.to_csv(filename, index=False)

    new_data2 = {'Timestamp': '', 'Python': [rest_of_data]}
    df_new2 = pd.DataFrame(new_data2)
    df = pd.concat([df, df_new2], ignore_index=True)
    # Write the updated DataFrame back to the CSV file
    df.to_csv(filename, index=False)
else:
    new_data2 = {'Timestamp': [current_time], 'Python': [speech]}
    df_new2 = pd.DataFrame(new_data2)
    df = pd.concat([df, df_new2], ignore_index=True)
    # Write the updated DataFrame back to the CSV file
    df.to_csv(filename, index=False)


    






print(speech)
print(f"Current Time: {current_time}")



