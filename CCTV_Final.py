#-*- coding: utf-8 -*-
import os, smtplib, time, datetime, sys
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email import Encoders
import random
import io
import picamera
import picamera.array
from time import localtime, strftime
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
    motionFound = random.randrange(0,2) == 0
    return motionFound
def write_video(stream):
    with io.open('before' + strftime("%Y-%m-%d %H-%M-%S",localtime()) + '.h264', 'wb') as output:
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
#--------------촬영 설정----------------------
gmail_user = "z331k7@gmail.com"
gmail_pwd = "tjdgus123"
def send_gmail(to, subject, message, attach):
    msg = MIMEMultipart('alternative')
    msg['From'] = "alarm"
    msg['To'] = to
    msg['Subject'] = subject
    msg.attach(MIMEText('<div>'+message+'</div>', 'html'))

    mailServer=smtplib.SMTP("smtp.gmail.com",587)
    mailServer.ehlo()
    mailServer.starttls()
    mailServer.ehlo()
    mailServer.login(gmail_user,gmail_pwd)
    mailServer.sendmail(gmail_user, to, msg.as_string())
    mailServer.close()


def mainLoop():
    message = sys.argv[1] if len(sys.argv)>1 else "%Y-%m-%d %H-%M-%S 집(현관)"
    title= sys.argv[2] if len(sys.argv)>2 else "CCTV에서 움직임 포착!"
    destination = "chejun99@gmail.com"
    print "[" + str(datetime.datetime.now()) + "] Sending mail to " + destination + "..."
    print "message : " + message
    print "title : " + title
    send_gmail(destination, title, message, "")
    print "[" + str(datetime.datetime.now()) + "] Complete..."

#-------------------------메일링 설정----------------
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
                camera.split_recording('after' + strftime("%Y-%m-%d %H-%M-%S",localtime()) + '.h264')
                write_video(stream)
                while detect_motion(camera, width, height):
                    camera.wait_recording(3)
                    print('Motion stopped!')
            camera.split_recording(stream)
            mainLoop()
            sleep(10)
    finally:
        camera.stop_recording()
