import speech_recognition as sr
import time
import winsound
from datetime import datetime
import pandas as pd

r = sr.Recognizer()

filename = '2-11-24.csv'

def delete_last_entry(df, filename):
    if not df.empty:
        df = df[:-1]  # Remove the last row
        df.to_csv(filename, index=False)
        print("Last entry deleted from the CSV file.")
    else:
        print("CSV file is empty. No entries to delete.")

df = pd.read_csv(filename)

mic = sr.Microphone()

#you are good to record beep
winsound.Beep(1000, 500)

with mic as source:
    audio = r.listen(source)

#recording has finished beep
winsound.Beep(700, 400)
#recording session info
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
speech = r.recognize_google(audio)

# Check if the word "delete" is spoken
if speech == 'delete last row':
    delete_last_entry(df, filename)
    print("Deletion logic executed.")

else:
    # Check if the length of speech is greater than 100 characters
    if len(speech) > 100:
        first_of_data = speech[:100]
        rest_of_data = speech[100:]

        # Append new data to the DataFrame
        new_data = {'Timestamp': [current_time], 'Python': [first_of_data]}
        df_new = pd.DataFrame(new_data)
        df = pd.concat([df, df_new], ignore_index=True)

        new_data2 = {'Timestamp': '', 'Python': [rest_of_data]}
        df_new2 = pd.DataFrame(new_data2)
        df = pd.concat([df, df_new2], ignore_index=True)

    else:
        new_data2 = {'Timestamp': [current_time], 'Python': [speech]}
        df_new2 = pd.DataFrame(new_data2)
        df = pd.concat([df, df_new2], ignore_index=True)

    # Write the updated DataFrame back to the CSV file
    df.to_csv(filename, index=False)

print(speech)
print(f"Current Time: {current_time}")
