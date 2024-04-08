# pip install opencv-python
import cv2


import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()



todays_date = datetime.now().strftime("%Y-%m-%d")

video_path = os.environ['VIDEO_PATH']

#vid_filename = video_path + "\timelapse_" + todays_date + index + ".avi"

def vid_indexer():
    index = []

    vid_filename = video_path + "\timelapse_" + todays_date + index + ".avi"
    return index

def record_video(base_path=video_path, width=640, height=480, fps=900.0):
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
    #cap = cv2.VideoCapture(0)
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame.")
            break

        # Our operations on the frame come here
       # frame = cv2.flip(frame, 1)

        # Write the flipped frame
        out.write(frame)

        # Display the resulting frame
        cv2.imshow('Preview: Press q to stop', frame)

        # Press 'q' to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    cap.release()
    out.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    record_video()


    """
def record_video(output_file='output.avi', width=640, height=480, fps=600.0):
    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(output_file, fourcc, fps, (width, height),isColor=False)
    
    # Capture video from the webcam
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame.")
            break
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Write the grayscale frame
        # Note: OpenCV expects a 3-channel image for color and 1-channel for grayscale for the `write` method,
        # since we initialized the writer with `isColor=False`, it expects a 1-channel image.
        out.write(gray_frame)

        # Display the resulting frame
        cv2.imshow('frame', gray_frame)

        # Press 'q' to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    cap.release()
    out.release()
    cv2.destroyAllWindows()
        """
