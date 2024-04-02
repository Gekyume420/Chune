import schedule
import time
import cv2
import os
# pip install schedule
num_of_existing_photos = 0


def count_files():
    files_in_dir = 0
    for filename in os.listdir():
        if filename.endswith('.png'):
            files_in_dir += 1
    return files_in_dir


def take_timestamp_photo():
    global num_of_existing_photos
    if num_of_existing_photos == 0:
        num_of_existing_photos = count_files()
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    timestamp = str(time.strftime("%Y/%m/%d-%H:%m"))
    font = cv2.FONT_HERSHEY_COMPLEX
    frame = cv2.putText(frame, timestamp, (425, 476), font, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
    filename = f'{num_of_existing_photos}.png'
    num_of_existing_photos += 1
    cv2.imwrite(f"{filename}", frame)


schedule.every(1).minutes.do(take_timestamp_photo)


while True:
    schedule.run_pending()
    time.sleep(1)
