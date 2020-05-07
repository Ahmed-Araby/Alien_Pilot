
import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BOARD)
GPIO.cleanup()

out_pins = [3, 5, 7, 33, 35, 37]

for pin in out_pins:
	GPIO.setup(pin , GPIO.OUT)



# run the motor forward 
#GPIO.output(33 ,GPIO.HIGH)
GPIO.output(5 , GPIO.LOW)
GPIO.output(7, GPIO.HIGH)
# pwm 
lp = GPIO.PWM(3, 100)
lp.start(80)

time.sleep(10)
GPIO.cleanup()

