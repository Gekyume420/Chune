# Chune
speech to text csv files


https://realpython.com/python-speech-recognition/


Next:
-Transmit the index # or “entry number” to the database, will help you sort through the data when coming through the web version of the data.

-Implement inverse square law feature w/r/t entries

-Update/change the ‘task’ column to read ‘thought log’ instead

-implement a feature that creates a new csv file automatically

-switch winsound to beepy 


~[this is an old idea -->] system that logs time spent under the umbrella of a certain task priority 
(e.g. you say "starting task HIGH at 3pm" and later on say "stopping task HIGH at 6pm", the system should be able to keep track of how many points that is worth)


Completed:
Work on 'start task' feature
        1) modify the 'end task' command to check if there is another string containing 'end task' above it(between the last start task), if so emit an error beep

        2) figure out a way to add the dt's(time differences) together and display them (i.e. print(total time spent 'in-task' = total_task_time)  )



input code that omits a different beep tone when the data isn't recorded right

stops recording if nothing is being recorded/transcribed (not sure yet which is causing it to freeze) after a certain lengeth of time.

Sync the csv files somehow so that nick and jackson can see each other progress. Add a username variable (e.g. if user name == nick, track the voice commands into columns 'Nick Timestamp')
        There may be a better way to do this but that is what came to mind



