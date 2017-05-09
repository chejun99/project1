#-*- coding: utf-8 -*-
import io
import random
import picamera
from PIL import Image
import time

prior_image = None
threshold = 10  # How Much pixel changes
sensitivity = 100  # How many pixels change
height = 1640
width = 1232


def detect_motion(camera):
    global prior_image
    stream = io.BytesIO()
    camera.capture(stream, format='jpeg', use_video_port=True)
    stream.seek(0)
    if prior_image is None:
        prior_image = Image.open(stream)
        return False
    else:
        current_image = Image.open(stream)
        if prior_image == current_iamge:
            print('sucess')
        result = random.randint(0, 10) == 0
        prior_image = current_image
        return result

def scanMotion(width, height):
    global sensitivity
    motionFound = False
    data1 = takeMotionImage(width, height)
    while not motionFound:
        data2 = takeMotionImage(width, height)
        diffCount = 0L
        for w in range(0, width):
            for h in range(0, height):
                # get the diff of the pixel. Conversion to int
                # is required to avoid unsigned short overflow.
                diff = abs(int(data1[h][w][1]) - int(data2[h][w][1]))
                if  diff > threshold:
                    diffCount += 1
            if diffCount > sensitivity:
                break; #break outer loop.
        if diffCount > sensitivity:
            motionFound = True
        else:
            data2 = data1              
    return motionFound


def takeMotionImage(width, height):
    with picamera.PiCamera() as camera:
        time.sleep(1)
        camera.resolution = (width, height)
        with picamera.array.PiRGBArray(camera) as stream:
            camera.exposure_mode = 'auto'
            camera.awb_mode = 'auto' 
            camera.capture(stream, format='rgb')
            return stream.array

def write_video(stream):
    with io.open('before.h264', 'wb') as output:
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
            if detect_motion(camera):
                print('Motion detected!')
                camera.split_recording('after.h264')
                write_video(stream)
                while detect_motion(camera):
                    camera.wait_recording(1)
                print('Motion stopped!')
                camera.split_recording(stream)
    finally:
        camera.stop_recording()
