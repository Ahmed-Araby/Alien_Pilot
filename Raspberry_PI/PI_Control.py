import RPi.GPIO as  GPIO

def convert_angle_command_to_pwm(angle):
	######
	# try to be continuous 
	return (angle + 1)/ 2  * (12 - 8) + 8
	#####
	"""
	# discrete output 
	if angle ==-2:
		return 8
	elif angle == -1:
		return 9
	elif angle == 0:
		return 10 # straight 
	elif angle ==  1:
		return 11
	return 12
	"""

def convert_speed_command_to_pwm(speed):
    speed = abs(speed)
    speed = speed  * 100  # convert speed from [0-1] to duty sycle precentage in range [0 , 100]
    return speed
    
def control_servo(servo, angle):
	angle_pwm_value = convert_angle_command_to_pwm(angle)
	servo.ChangeDutyCycle(angle_pwm_value)
	return 

# PWM
def control_DC_motors(speed, DC_motors_state,left_DC, right_DC, left_motor_pins , right_motor_pins):
    # try to save using the GPIO pins as this would increase the lag on the communication 
    if speed >=0 and DC_motors_state !='forward':
        DC_motors_state = 'forward'
        drive_forward(True, True, left_motor_pins, right_motor_pins);
    if speed <0 and DC_motors_state!='backward':
        DC_motors_state = 'backward'
        drive_backward(True, True, left_motor_pins, right_motor_pins);
        
    speed_pwm_value = convert_speed_command_to_pwm(speed)
    left_DC.ChangeDutyCycle(speed_pwm_value)
    right_DC.ChangeDutyCycle(speed_pwm_value)
    
    return DC_motors_state

def set_enable_pins(enable_pins, value = GPIO.OUT):
	print(" DC motors Enbale pins are set to :", value)
	for pin in enable_pins:
		GPIO.setup(pin, value)
	return 

def drive_forward(left_motor , right_motor, left_motor_pins, right_motor_pins):
	if left_motor:
		# as the normal  table
		GPIO.output(left_motor_pins[0], GPIO.HIGH)
		GPIO.output(left_motor_pins[1], GPIO.LOW)
	if right_motor:
		# reverse of the normal table 
		GPIO.output(right_motor_pins[0], GPIO.LOW)
		GPIO.output(right_motor_pins[1], GPIO.HIGH)
	return 
    
def drive_backward(left_motor, right_motor, left_motor_pins, right_motor_pins):
    	if left_motor:
		# as the normal  table
		GPIO.output(left_motor_pins[0], GPIO.LOW)
		GPIO.output(left_motor_pins[1], GPIO.HIGH)
	if right_motor:
		# reverse of the normal table 
		GPIO.output(right_motor_pins[0], GPIO.HIGH)
		GPIO.output(right_motor_pins[1], GPIO.LOW)
	return 

def brake(left_motor, right_motor,left_motor_pins, right_motor_pins):
	if left_motor:
		GPIO.output(left_motor_pins[0], GPIO.LOW)
		GPIO.output(left_motor_pins[1], GPIO.LOW)
	if right_motor:
		GPIO.output(right_motor_pins[0], GPIO.LOW)
		GPIO.output(right_motor_pins[1], GPIO.LOW)
	return 







# main 
if __name__ == "__main__":
    # for testing 
	GPIO.setmode(GPIO.BOARD)
	output_left_pins = [3, 5, 7]
	output_right_pins = [33, 35, 37]

	set_enable_pins(output_left_pins + output_right_pins)

	drive_forward(True, True, output_left_pins, output_right_pins)

	import time 
	time.sleep(100)

	GPIO.cleanup()

