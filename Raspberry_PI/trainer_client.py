# client.py
# been edited for trainig 
import io
import socket
import struct
import time
import picamera
import RPi.GPIO as GPIO
from PI_Control import *

def write_img_to_stream(stream):
	global DC_motors_state
	# SEND image size 
	client_socket.send(struct.pack('<L' , stream.tell()))

	# SEND image 
	stream.seek(0)
	client_socket.sendall(stream.read())
	# I have to include this other wise 
	# the buffer will be filled and loop in server will not break 
	respond2 = client_socket.recv(struct.calcsize('i'))
	
	# get the control data 
	control_data_bytes = client_socket.recv(struct.calcsize('ff'))
	angle , speed = struct.unpack('ff' , control_data_bytes)
	#print("angle is {} , speed is {}".format(angle , speed))
	
	
	# send control to the servo 
	control_servo(servo , angle)
        # send control to the DC motors 
	DC_motors_state = control_DC_motors(speed, DC_motors_state,left_DC, right_DC, output_left_pins, output_right_pins)
	
	# delete the stream 
	stream.seek(0)
	stream.truncate()
        return 

def gen_seq():
    stream = io.BytesIO()
    while True:
        yield stream
	#print(stream.tell())
        write_img_to_stream(stream)

################################################################# GPIO stuff  ######################################################
GPIO.setmode(GPIO.BOARD)
# servo stuff 
GPIO.setup(11 , GPIO.OUT)
servo = GPIO.PWM(11, 50)
servo.start(10) # straight 

# DC motors stuff 
# input pins 
output_left_pins = [5, 7]
output_right_pins = [35, 37]
set_enable_pins(output_left_pins + output_right_pins)
# pmw for the enable pins 
DC_motors_state = 'brake'
GPIO.setup(3 , GPIO.OUT)
GPIO.setup(33, GPIO.OUT)
left_DC = GPIO.PWM(3 , 100)
right_DC = GPIO.PWM(33, 100)
# hold the motors 
left_DC.start(0)
right_DC.start(0)
################################################################# end of GPIO stuff #################################################

################################################################# socket stuff #################################################
client_socket = socket.socket()
# get buffer size 
buff_size = client_socket.getsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF)
print("buffer size  is {}".format(buff_size))

IP_Address = "192.168.1.6"  # it should be changed every time  
Port = 1234
client_socket.connect( ( IP_Address, Port) )
################################################################# end of socket stuff #################################################

try:
    with picamera.PiCamera() as camera:
	print("start client")
        camera.resolution = (227 , 227 ) # width , height

        # Start a preview and let the camera warm up for 2 seconds
        camera.start_preview()
        time.sleep(2)
        camera.stop_preview()

        print(" start ")
        print("running in default")
        camera.capture_sequence(gen_seq(), "jpeg", use_video_port=True)
    

finally:
    client_socket.close()
    servo.stop()
    GPIO.cleanup()

print("client is dead")
