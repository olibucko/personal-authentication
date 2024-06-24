# Import dependencies
import cv2
import mediapipe as mp

# MediaPipe objects
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

# Gesture to authenticate
gesture_auth = ["Closed", "Open", "Closed", "Closed", "Open"]

def main():
  # Produce video stream
  cap = cv2.VideoCapture(0)

  # Initialize MediaPipe with desired settings
  with mp_hands.Hands(model_complexity=1, max_num_hands = 1, min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
    while cap.isOpened():
      # Process the image frame by frame. Store each frame in the 'image' variable and error check.
      success, image = cap.read()
      if not success:
        print("Ignoring empty camera frame.")
        # If loading a video, use 'break' instead of 'continue'.
        continue

      # To improve performance, optionally mark the frame as not writeable to pass by reference.
      image.flags.writeable = False

      # Convert frame to the OpenCV/MediaPipe compatible BGR colour space.
      image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

      # Process the frame using MediaPipe model and assign the output data to "results" object.
      results = hands.process(image)

      # Make the frame writeable again. Convert back to RGB colour space for our later use.
      image.flags.writeable = True
      image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

      
      # Perform the processing we want for the application.
      processed = hand_processing(image, results)
        
      # Flip the frame horizontally for a selfie-view display.
      final_image = cv2.flip(image, 1)
      cv2.imshow('MediaPipe Hands', final_image)

      # Display information on the screen.
      (x, y, windowWidth, windowHeight) = cv2.getWindowImageRect("MediaPipe Hands")
      org = (x,y)
      colour = (117, 223, 109)
      final_image = cv2.putText(final_image, str(processed), org, 2, 0.5, colour, 2, 2, False)

      cv2.imshow('MediaPipe Hands', final_image)
    
      if cv2.waitKey(5) & 0xFF == 27:
        break
      
      if processed == gesture_auth:
        break
    
  cap.release()


def hand_processing(image, results):
    # Create iterable hand landmark object
    hand_landmarks = results.multi_hand_landmarks
    # Create handedness variable to store whether the relevant hand is left or right
    handedness = ""

    if results.multi_hand_landmarks:
        # Determine if a left or right hand is in the frame.
        for hand in results.multi_handedness:
            classification = ["Right hand", "Left hand"]
            index = hand.classification[0].index
            handedness = classification[index]
            print(handedness)

        for hand_landmark in hand_landmarks:
            # Determine numerical finger status. Using these values you can associate "Open" or "Closed" states.
            # Perform special checking in the case of the thumb finger.
            if handedness == "Right hand":
                thumb_position = hand_landmark.landmark[4].x - hand_landmark.landmark[2].x
            elif handedness == "Left hand":
                thumb_position = -(hand_landmark.landmark[4].x - hand_landmark.landmark[2].x)
            else:
                print("Error")

            pointer_position = hand_landmark.landmark[8].y - hand_landmark.landmark[5].y
            middle_position = hand_landmark.landmark[12].y - hand_landmark.landmark[9].y
            ring_position = hand_landmark.landmark[16].y - hand_landmark.landmark[13].y
            pinky_position = hand_landmark.landmark[20].y - hand_landmark.landmark[17].y

            position_array = [thumb_position, pointer_position, middle_position, ring_position, pinky_position]
            state_array = []

            # Associate "Open" or "Closed" finger states.
            for finger in position_array:
                # Assign correct state (if the finger is not the thumb)
                if finger < 0 and finger != position_array[0]:
                    state_array.append("Open")
                elif finger > 0 and finger != position_array[0]:
                    state_array.append("Closed")

                # Assign correct state (if the finger is the thumb)
                elif finger < 0 and finger == position_array[0]:
                    state_array.append("Closed")
                elif finger > 0 and finger == position_array[0]:
                    state_array.append("Open")
                else:
                    state_array.append("Unknown/Error")

            # print(state_array)

            # Draw hand landmarks on the frame for visual reference
            mp_drawing.draw_landmarks(image, hand_landmark, mp_hands.HAND_CONNECTIONS, mp_drawing_styles.get_default_hand_landmarks_style(), mp_drawing_styles.get_default_hand_connections_style())
            return(state_array)

