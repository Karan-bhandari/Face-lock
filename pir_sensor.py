import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

GPIO.setup(12, GPIO.IN) #PIR
GPIO.setup(7, GPIO.OUT) #BUzzer

try:
    time.sleep(2) # to stabilize sensor
    while True:
        if GPIO.input(12):
            GPIO.output(7, True)
            time.sleep(0.5) #Buzzer turns on for 0.5 sec
            GPIO.output(7, False)
            print("Motion Detected...")
            time.sleep(2) #to avoid multiple detection
        time.sleep(0.1) #loop delay, should be less than detection delay

except:
    GPIO.cleanup()