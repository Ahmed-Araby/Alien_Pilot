import pygame
import os
from constants import *
import pandas as pd
import sys
import cv2

def disp(img):
    cv2.imshow('' , img)
    cv2.waitKey()
    cv2.destroyAllWindows()
    pass
def convert_to_command(axis_value):
    return axis_value
    if axis_value <= - 0.55:
        return -2  # very left
    elif axis_value <= - 0.1:
        return -1  # left
    elif axis_value <= 0.1:
        return 0  # right
    elif axis_value <= 0.55:
        return 1  # right
    return 2  # very right



def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.K_ESCAPE:
            print("Exit")
            sys.exit()
        if event.type == pygame.JOYAXISMOTION:
            #print("Axis motion")
            pass


def save_training_data(frames, angles, speed=None):
    images_names = os.listdir('./data/images')
    ID = len(images_names)
    images_paths = []
    for i in range(0 , len(frames),1):
        image_name = str(ID) + '.jpeg'
        image_path = os.path.join("data/images", image_name)
        images_paths.append(image_path)
        cv2.imwrite(image_path, frames[i])
        ID +=1

    tmp_dic = {'path':images_paths, 'angle':angles}
    data_frame = pd.DataFrame(tmp_dic)
    data_frame.to_csv("data/data.csv", header=True)
    return