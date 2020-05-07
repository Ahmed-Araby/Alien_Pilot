import argparse
import base64
from datetime import datetime
import os
import shutil
import numpy as np
import socketio
import eventlet
import eventlet.wsgi
from PIL import Image
from flask import Flask
from io import BytesIO
from keras.models import load_model
from keras.optimizers import  Adam
import h5py
from keras import __version__ as keras_version
from PID import PID_Controller

sio = socketio.Server()
app = Flask(__name__)
model = None
prev_image_array = None


class SimplePIController:
    def __init__(self, Kp, Ki):
        self.Kp = Kp
        self.Ki = Ki
        self.set_point = 0.
        self.error = 0.
        self.integral = 0.

    def set_desired(self, desired):
        self.set_point = desired

    def update(self, measurement):
        # proportional error
        self.error = self.set_point - measurement

        # integral error
        self.integral += self.error

        return self.Kp * self.error + self.Ki * self.integral


        
controller = PID_Controller(0.1, 0.002,0.005, 10) 
set_speed = 15

"""
# udacity code 
controller = SimplePIController(0.1, 0.002)
controller.set_desired(set_speed)
"""


###############################################
# preprocessing

def crop_img(img):
    H , W , _ = img.shape
    img = img[40:H-20, :, :]
    return img

def normalize_img_0_1(img):
  img = img /255.0
  img = img.astype(np.float32) # less memory
  return img

def preprocessing_pipeline(img):
    img = normalize_img_0_1(img)
    #img = resize_img(img) 
    img = crop_img(img)
    return img


# speed sequence
speed_seq = [.2]*20
def update_seq(speed):
    global speed_seq
    speed_seq = speed_seq[1:]
    speed_seq.append(speed)
    return

###############################################

@sio.on('telemetry')
def telemetry(sid, data):
    if data:
        # The current steering angle of the car
        steering_angle = data["steering_angle"]
        # The current throttle of the car
        throttle = data["throttle"]
        # The current speed of the car
        speed = data["speed"]
        # The current image from the center camera of the car
        imgString = data["image"]
        image = Image.open(BytesIO(base64.b64decode(imgString)))
        image_array = np.asarray(image)
        # steering_angle = float(model.predict(image_array[None, :, :, :], batch_size=1))\

        ########################################################
        image_array = preprocessing_pipeline(image_array)

        steering_angle , speed_out = model.predict([image_array[None , : , : , :] , np.array(speed_seq).reshape(-1, 20, 1)] , batch_size = 1)
        steering_angle = float(steering_angle)
        speed_out = float(speed_out)
        
        update_seq(speed_out)
        ########################################################

        #throttle = controller.update(float(speed))
        # this speed is comming from the simulator which mean it's the actual dammen speed 
        throttle = controller.update_speed(speed_out * 30, float(speed))
        
        print(steering_angle, speed_out * 30, throttle)
        send_control(steering_angle, throttle)

        # save frame
        if args.image_folder != '':
            timestamp = datetime.utcnow().strftime('%Y_%m_%d_%H_%M_%S_%f')[:-3]
            image_filename = os.path.join(args.image_folder, timestamp)
            image.save('{}.jpg'.format(image_filename))
    else:
        # NOTE: DON'T EDIT THIS.
        sio.emit('manual', data={}, skip_sid=True)


@sio.on('connect')
def connect(sid, environ):
    print("connect ", sid)  
    send_control(0, 0)


def send_control(steering_angle, throttle):
    sio.emit(
        "steer",
        data={
            'steering_angle': steering_angle.__str__(),
            'throttle': throttle.__str__()
        },
        skip_sid=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Remote Driving')
    parser.add_argument(
        'model',
        type=str,
        help='Path to model h5 file. Model should be on the same path.'
    )
    parser.add_argument(
        'image_folder',
        type=str,
        nargs='?',
        default='',
        help='Path to image folder. This is where the images from the run will be saved.'
    )
    args = parser.parse_args()

    # check that model Keras version is same as local Keras version
    f = h5py.File(args.model, mode='r')
    model_version = f.attrs.get('keras_version')
    keras_version = str(keras_version).encode('utf8')

    if model_version != keras_version:
        print('You are using Keras version ', keras_version,
              ', but the model was built using ', model_version)

    model = load_model(args.model, compile=False)
    if args.image_folder != '':
        print("Creating image folder at {}".format(args.image_folder))
        if not os.path.exists(args.image_folder):
            os.makedirs(args.image_folder)
        else:
            shutil.rmtree(args.image_folder)
            os.makedirs(args.image_folder)
        print("RECORDING THIS RUN ...")
    else:
        print("NOT RECORDING THIS RUN ...")

    # wrap Flask application with engineio's middleware
    app = socketio.Middleware(sio, app)

    # deploy as an eventlet WSGI server
    eventlet.wsgi.server(eventlet.listen(('', 4567)), app)