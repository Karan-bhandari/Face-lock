# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import imutils
import pickle
import face_recognition
import argparse
import RPi.GPIO as GPIO

#Assigning the pins to the sensors ans servo
GPIO.setmode(GPIO.BOARD)
GPIO.setup(40, GPIO.IN, pull_up_down=GPIO.PUD_UP) #Inside button for exit
GPIO.setup(10, GPIO.OUT) #Servo
GPIO.setup(12, GPIO.IN) #PIR
p = GPIO.PWM(10, 50)
p.start(7.5) #Set position to 90 degrees

 
# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (320, 240)
camera.framerate = 15
rawCapture = PiRGBArray(camera, size=(320, 240))
 
# allow the camera to warmup
time.sleep(0.1)

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-c", "--cascade", required=True,
    help = "path to where the face cascade resides")
ap.add_argument("-e", "--encodings", required=True,
    help="path to serialized db of facial encodings")
args = vars(ap.parse_args())


print("[INFO] loading encodings + face detector...")
data = pickle.loads(open(args["encodings"], "rb").read())
detector = cv2.CascadeClassifier(args["cascade"])

print("[INFO] starting video stream...")

while(True) :
    if GPIO.input(12):
        print("bhoot aaya")
        #p.ChangeDutyCycle(10.5)
        #time.sleep(3)
        #p.ChangeDutyCycle(7.5)
        # capture frames from the camera
        flag1 = True
        if flag1 == True:
            for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
                if flag1 == False :
                    break
                # grab the raw NumPy array representing the image, then initialize the timestamp
                # and occupied/unoccupied text
                #frame = imutils.resize(frame, width=500)
                image = frame.array
                gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
                rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                
                faces = detector.detectMultiScale(gray, 1.1, 5)
                boxes = [(y, x + w, y + h, x) for (x, y, w, h) in faces]
                
                encodings = face_recognition.face_encodings(rgb, boxes)
                names = []
                p.ChangeDutyCycle(7.5)
                print("First")
                input_state = GPIO.input(40)
                if input_state == False:
                    print("pressed and going out")
                    p.ChangeDutyCycle(10.5)
                    time.sleep(5)
                    p.ChangeDutyCycle(7.5)
                
                for encoding in encodings:
                    # attempt to match each face in the input image to our known
                    # encodings
                    matches = face_recognition.compare_faces(data["encodings"],
                        encoding)
                    name = "Unknown"
                    print("Second")
                    
                
                    

                    # check to see if we have found a match
                    if True in matches:
                        # find the indexes of all matched faces then initialize a
                        # dictionary to count the total number of times each face
                        # was matched
                        print("Third")
                        matchedIdxs = [i for (i, b) in enumerate(matches) if b]
                        counts = {}

                        # loop over the matched indexes and maintain a count for
                        # each recognized face face
                        for i in matchedIdxs:
                            name = data["names"][i]
                            counts[name] = counts.get(name, 0) + 1

                        # determine the recognized face with the largest number
                        # of votes (note: in the event of an unlikely tie Python
                        # will select first entry in the dictionary)
                        name = max(counts, key=counts.get)
                    
                        
                    # update the list of names
                    print("Fourth")
                    names.append(name)
                    
                    for ((top, right, bottom, left), name) in zip(boxes, names):
                    # draw the predicted face name on the image
                        print("Five")
                        cv2.rectangle(image, (left, top), (right, bottom),
                            (0, 255, 0), 2)
                        y = top - 15 if top - 15 > 15 else top + 15
                        cv2.putText(image, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
                            0.75, (0, 255, 0), 2)
                        if name == "Unknown":
                            print("Unknown person detected, DO NOT OPEN THE DOOR")
                            p.ChangeDutyCycle(7.5)
                            flag1 = False
                            break
                        else:
                            print(name, "detected, should now send signal to open door")
                            
                            """if input_state == False:
                                  print("pressed and going out")"""
                            p.ChangeDutyCycle(10.5)
                            time.sleep(5)
                            p.ChangeDutyCycle(7.5)

                # display the image to our screen
                cv2.imshow("Frame", image)
                key = cv2.waitKey(1) & 0xFF 
                # clear the stream in preparation for the next frame
                rawCapture.truncate(0)
             
                # if the `q` key was pressed, break from the loop
                if key == ord("q"):
                    break



