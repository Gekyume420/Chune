import cv2
import os
from datetime import datetime
import time

def record_timelapse(base_path='C:\\Users\\16198\\Documents\\PYTHON\\Timelapse', width=1920, height=1080, fps=30.0):
    # Time-lapse parameters
    hours_per_30_seconds_video = 1
    real_time_seconds_per_hour = 3600
    desired_video_length_seconds = 12
    capture_interval = real_time_seconds_per_hour / (desired_video_length_seconds * fps) # Every 4 seconds

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
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    last_frame_time = time.time() - capture_interval

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame.")
            break
        
        current_time = time.time()
        if current_time - last_frame_time >= capture_interval:
            last_frame_time = current_time
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cv2.putText(frame, timestamp, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            out.write(frame)

        cv2.imshow("Timelapse", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    record_timelapse()
