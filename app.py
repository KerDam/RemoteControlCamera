from flask import Flask, render_template, Response
from imutils.video import VideoStream
from flask_nav import Nav
from flask_nav.elements import Navbar, Subgroup, Text, View
from flask_bootstrap import Bootstrap
from camera import VideoCamera
import cv2
import argparse
import datetime
import imutils
import time

app = Flask(__name__)
nav = Nav(app)
Bootstrap(app)

@nav.navigation('site_navbar')
def create_navbar():
    home_view = View('Home', 'home')
    live_view = View('Live','live',status=0) #init with OFF state of the webcam
    gallery_view = View('Gallery','gallery')
    return Navbar('RemoteCamera', home_view, live_view, gallery_view)

@app.route('/')
def home():
    return render_template('base.html')

    
@app.route('/live/<int:status>')
def live(status):
    #return render_template('live.html')
    if status:        
        return render_template('live.html', status=status)
    else:        
        return render_template('live.html', status=status)
    

@app.route('/gallery')
def gallery():
    return render_template('live.html')
  
# Webcam handling

def gen(camera):
    
    firstFrame = None

    while True:
        frame = camera.get_jpg_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        
        
        frame = camera.get_frame()

        # if the frame could not be grabbed, then we have reached the end
        # of the video
        if frame is None:
            break

        # resize the frame, convert it to grayscale, and blur it
        frame = imutils.resize(frame, width=500)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        # if the first frame is None, initialize it
        if firstFrame is None:
            firstFrame = gray
            continue

        # compute the absolute difference between the current frame and
        # first frame
        frameDelta = cv2.absdiff(firstFrame, gray)
        thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]

        # dilate the thresholded image to fill in holes, then find contours
        # on thresholded image
        thresh = cv2.dilate(thresh, None, iterations=2)
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)

        # loop over the contours
        for c in cnts:
            # if the contour is too small, ignore it
            if cv2.contourArea(c) < 500:
                continue
            print("Occupied")

            
    frame = camera.get_frame()
    yield (b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
    
@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
