import io
import socket
import struct
import cv2
import numpy as np
import pygame
from Drawer import *
from utils import *
import time

if __name__ == '__main__':

    print("START SERVER")
    ####### pygame #######
    drawer = Drawer()
    joy = pygame.joystick.Joystick(0)
    joy.init()
    ####### end of pygame #######

    ####### socket ########
    server_socket = socket.socket()
    server_socket.bind((IP_Address, Port))
    server_socket.listen(1)
    client_socket , address = server_socket.accept()
    ###### end of socket #######


    ###### recording data set  ######
    frames = []
    angles = []
    ###### end of recording data set ######

    try:
        # main loop for the GUI and for the connection
        while True:
            ############################################## recieving #######################################################
            begin = time.time()
            image_len_bytes = client_socket.recv(struct.calcsize('<L'))
            image_len = struct.unpack('<L' , image_len_bytes)[0]

            if not image_len:
                break

            image_stream = io.BytesIO()
            image_bytes = bytearray()
            cnt = 0
            while True:
                fragment = client_socket.recv(image_len)
                cnt+=len(fragment)
                image_bytes.extend(fragment)
                if cnt==image_len:
                    break

            client_socket.send(struct.pack('i', 2))  # tell the pi that I did recived the image
            image_stream.write(image_bytes)
            image_stream.seek(0)
            ############################################### end of receving ###################################################


            ############################################### cv2 part ##########################################################
            file_bytes = np.asarray(bytearray(image_stream.read()), dtype=np.uint8)
            image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
            image  = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            ############################################### end of cv2 part ###################################################


            ############################################### pygame part ########################################################
            handle_events()
            steering_angle= joy.get_axis(0)
            steering_angle = round(steering_angle, 2)
            speed = -1 * joy.get_axis(3)
            speed = round(speed, 2)
            #print(speed)
            drawer.draw_screen(image, steering_angle, 1)
            ################################################ end pygame part ####################################################


            ############################################### send control data to pi #############################################
            control_data_bytes = struct.pack('ff' , steering_angle, speed)
            client_socket.send(control_data_bytes)
            ############################################### end of sending control ##############################################


            ############################################### record trainign data   ##############################################
            """
            frames.append(image)
            angles.append(steering_angle)
            if len(angles) >= MAX_number_of_frames:
                print("RECORDING THE DATA SET")
                save_training_data(frames, angles)
                frames = []
                angles = []
            """
            #print("time for frame {}".format(time.time()-begin))


    finally:
        client_socket.close()
        server_socket.close()

print("SERVER IS DEAD")