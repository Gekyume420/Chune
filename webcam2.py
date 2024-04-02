import cv2


import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
import time
load_dotenv()



todays_date = datetime.now().strftime("%Y-%m-%d")

video_path = os.environ['VIDEO_PATH']

#vid_filename = video_path + "\timelapse_" + todays_date + index + ".avi"

def vid_indexer():
    index = []

    vid_filename = video_path + "\timelapse_" + todays_date + index + ".avi"
    return index

def record_timelapse(base_path=video_path, width=640, height=480, fps=20.0, capture_interval=1):
    # Generate the base filename with today's date
    today = datetime.now().strftime("%Y-%m-%d")
    filename = f"Timelapse_{today}"
    file_number = 0
    output_file = f"{filename}.avi"

    # Check if the file already exists and update the filename accordingly
    while os.path.exists(os.path.join(base_path, output_file)):
        file_number += 1
        output_file = f"{filename}_{file_number}.avi"

    # Full path to the output file
    full_output_path = os.path.join(base_path, output_file)
    
    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(full_output_path, fourcc, fps, (width, height))
    
    # Capture video from the webcam
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    last_frame_time = time.time() - capture_interval

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame.")
            break

        # Overlay timestamp on every frame for display
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        display_frame = frame.copy()
        cv2.putText(display_frame, timestamp, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        # Check if it's time to capture the frame for the timelapse
        current_time = time.time()
        if current_time - last_frame_time >= capture_interval:
            last_frame_time = current_time

            # Write the original frame (without the updated timestamp) for consistency in the timelapse
            out.write(frame)

        # Display the frame with the timestamp
        cv2.imshow('frame', display_frame)

        # Press 'q' to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    cap.release()
    out.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    record_timelapse()
