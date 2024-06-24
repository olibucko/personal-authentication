import gesture_recognition

user = "Oliver"


def app():
  # Call facial recognition here

  print("Facial recognition successful...")
  print("Hi " + user + " please provide the authentication gesture")
  gesture_recognition.main()
  print("Gesture authenticated...")
  print("Welcome back")

app()