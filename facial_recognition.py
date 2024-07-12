import face_recognition
import cv2
import numpy as np
import time
import datetime
import os
import sys

################## DEFINE GLOBAL VARIABLE ######################

device_locked = False
run_program = True

################## DEFINE FUNCTIONS ######################

def countdown(h, m, s):
      total_seconds = h * 3600 + m * 60 + s

      while total_seconds > 0:
            timer = datetime.timedelta(seconds = total_seconds)

            print(timer, end="\r")

            # Delays the program one second
            time.sleep(1)

            # Reduces total time by one second
            total_seconds -= 1

      print("Timer countdown complete")

def f_recog():
    global device_locked
    # Get a reference to webcam #0 (the default one)
    video_capture = cv2.VideoCapture(0)

    # Create arrays of known face encodings and their names
    known_face_encodings = [
        
    ]

    known_face_names = [
        "Oliver",
    ]

    for name in known_face_names:
        user_image = face_recognition.load_image_file("People/" + name + ".jpg")
        user_face_encoding = face_recognition.face_encodings(user_image)[0]
        known_face_encodings.append(user_face_encoding)
        print("Successful encoding of " + name + " into the program.")

    # Initialize some variables
    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True

    while True:
        # Grab a single frame of video
        ret, frame = video_capture.read()

        # Only process every other frame of video to save time
        if process_this_frame:
            # Resize frame of video to 1/4 size for faster face recognition processing
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

            # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
            
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            face_names = []
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"

                # If a match was found in known_face_encodings, just use the first one.
                if True in matches:
                    first_match_index = matches.index(True)
                    name = known_face_names[first_match_index]

                # Or instead, use the known face with the smallest distance to the new face
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]

                face_names.append(name)

        process_this_frame = not process_this_frame


        # Display the results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        # Display the resulting image
        cv2.imshow('Video', frame)

        # Perform authentication logic
        if type(face_names) is list and type("Oliver") is str:
            if device_locked == False:
                if "Oliver" in face_names:
                    print("Successful authentication this frame.")
                elif "Oliver" not in face_names:
                    print("Device lock countdown intiated.")
                    countdown(0,0,5)
                    print("DEVICE LOCKED")
                    os.system("gnome-screensaver-command -a")
                    device_locked = True
                    break
                else:
                    print("This should not be happening. Error.")

            if device_locked == True:
                if "Oliver" in face_names:
                    print("Unlocking device.")
                    os.system("gnome-screensaver-command -d")
                    device_locked = False
                elif "Oliver" not in face_names:
                    print("Keeping device locked.")
                    continue
                else:
                    print("This should not be happening. Error.")
        else:
            print("Data failed to pass quality checks.")
            return

        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            video_capture.release()
            cv2.destroyAllWindows()
            break

################## APPLICATION LOGIC ######################

if __name__ == "__main__":
    while run_program == True:
        if f_recog() == None:
            
            # Find state of the lock screen and assign to variable
            if os.system("gnome-screensaver-command -q") != "The screensaver is inactive":
                device_locked = True
            elif os.system("gnome-screensaver-command -q") == "The screensaver is inactive":
                device_locked = False

            f_recog()
            
    
