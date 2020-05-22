import RPi.GPIO as GPIO
import time
#from time import sleep, strftime, time
GPIO.setmode(GPIO.BOARD)

GPIO.setup(12, GPIO.IN) #PIR
GPIO.setup(10, GPIO.OUT) #Servo

p = GPIO.PWM(10, 50)
p.start(7.5) #Set servo to 90 degrees



with open("/home/pi/Desktop/log123.csv", "a") as log:
    time.sleep(2)
    try:
        while(True):
            if GPIO.input(12):
                p.ChangeDutyCycle(10.5)
                log.write("{0},Door Unlocked \n".format(strftime("%d-%m-%Y %H:%M:%S")))
                time.sleep(3)
                p.ChangeDutyCycle(7.5)
            time.sleep(0.1)
    
    except:
        GPIO.cleanup()