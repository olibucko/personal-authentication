def userCheck(face_names, accepted):
      if type(face_names) is list and type(accepted) is str:
            if accepted in face_names:
                  print("Successful authentication")
            else:
                  print("Failure to authenticate")
      else:
            print("One or more arguments for userCheck() are not lists or strings.")
            return
      
# Make failure to authenticate trigger a timer that counts down from 10s. On 10s the "lock" is triggered.