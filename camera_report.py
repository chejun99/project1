#-*- coding: utf-8 -*-
import random
import io
import picamera
import picamera.array
import datetime
import time
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from fractions import Fraction

prior_image = None
threshold = 20  # How Much pixel changes
height = 1280
width = 720
sensitivity = height*width*0.1  # How many pixels change


def detect_motion(camera, width, height):
    global prior_image
    stream = io.BytesIO()
    camera.capture(stream, format='jpeg', use_video_port=True)
    stream.seek(0)
    if prior_image is None:
        prior_image = Image.open(stream).load()
        return False
    else:
        current_image = Image.open(stream).load()
        result = scanMotion(width, height, current_image, prior_image)
        prior_image = current_image
        return result

def scanMotion(width, height, current_image, prior_image):
    print("scanMotion initiated")
    global threshold
    global sensitivity
    motionFound = False
    diffCount = 0L
    for w in range(0, width):
        for h in range(0, height):
            diff = abs(int(prior_image[h, w][1]) - int(current_image[h, w][1]))
            if  diff > threshold:
                diffCount += 1
        if diffCount > sensitivity:
            motionFound = True
            break
    print ("diffCount : ",diffCount)
    return motionFound
#
#
# def takeMotionImage(width, height):
#     with picamera.PiCamera() as camera:
#         time.sleep(1)
#         camera.resolution = (width, height)
#         with picamera.array.PiRGBArray(camera) as stream:
#             camera.exposure_mode = 'auto'
#             camera.awb_mode = 'auto'
#             camera.capture(stream, format='rgb')
#             return stream.array

def write_video(stream):
    with io.open('before',strftime("%Y-%M-%D %h-%m-%s",localtime()),'.h264', 'wb') as output:
        for frame in stream.frames:
            if frame.header:
                stream.seek(frame.position)
                break
        while True:
            buf = stream.read1()
            if not buf:
                break
            output.write(buf)
    stream.seek(0)
    stream.truncate()

with picamera.PiCamera() as camera:
    camera.resolution = (1280, 720)
    stream = picamera.PiCameraCircularIO(camera, seconds=10)
    camera.start_recording(stream, format='h264')
    try:
        while True:
            camera.wait_recording(1)
            print("calling detect_motion in main loop:")
            if detect_motion(camera, width, height):
                print('Motion detected!')
                camera.split_recording('after',strftime("%Y-%M-%D %h-%m-%s",localtime()),'.h264')
                write_video(stream)
                while detect_motion(camera, width, height):
                    camera.wait_recording(3)
                print('Motion stopped!')
                camera.split_recording(stream)
    finally:
        camera.stop_recording()
        #aa
