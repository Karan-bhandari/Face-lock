import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setup(40, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(10, GPIO.OUT)

#pin 10 and 50Hz
p = GPIO.PWM(10, 50)
p.start(7.5)


while True:
    input_state = GPIO.input(40)
    if input_state == False:
          print("press")
          p.ChangeDutyCycle(10.5)
          time.sleep(3)
          p.ChangeDutyCycle(7.5)
        