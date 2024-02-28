from datetime import datetime
from dotenv import load_dotenv
from src.db import DB
from src.stt import STT
import os
import pandas as pd
import pyfiglet
from quo import echo
import uuid


load_dotenv()

# Dynamic unique identifier based on MAC address
COMPUTER_ID = uuid.UUID(int=uuid.getnode()).hex[-12:]

# database initialization
database_url = os.environ['DATABASE_URL']
credentials_path = os.environ['CREDENTIALS_PATH']
db = DB(database_url, credentials_path)

# speech-to-text
stt = STT()


if __name__ == "__main__":
    print(pyfiglet.figlet_format("Tandem", font=f"slant"))

    input("Press any key to record task")
    print("Listening...")
    text = stt.recognize()
    print(f"Task recorded ->", end=" ")
    echo(text, italic=True)


    path = f'/tasks/{datetime.now().strftime("%Y-%m-%d")}/{COMPUTER_ID}'
    task_data = {"task": text, "time": datetime.now().strftime("%H:%M:%S")}

    db.insert(path, task_data)

    all_task_data = list(db.get(path).values())
    all_task_data.sort(key=lambda x: x['time'])

    print(pd.DataFrame(all_task_data).to_markdown(tablefmt="rounded_outline"))
