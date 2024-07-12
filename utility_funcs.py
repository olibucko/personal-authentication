import time
import datetime

def userCheck(face_names, accepted):
      if type(face_names) is list and type(accepted) is str:
            if accepted in face_names:
                  print("Successful authentication.")
            elif accepted not in face_names:
                  print("Device lock countdown intiated.")
                  countdown(0,0,5)
                  print("DEVICE LOCK")
            else:
                  print("No faces in the frame.")
      else:
            print("One or more arguments for userCheck() are not lists or strings.")
            return
      
# Countdown is looping because camera moves on to next recorded frame instead of jumping to new, most recent frame.

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
