from flask import Flask, render_template, Response, session, request, session, flash, abort, redirect
from imutils.video import VideoStream
from flask_nav import Nav
from flask_nav.elements import Navbar, Subgroup, Text, View
from flask_bootstrap import Bootstrap
from camera import VideoCamera
import cv2
import os
from sqlalchemy.orm import sessionmaker
from tabledef import *

import argparse
import datetime
import imutils
import time

engine = create_engine('sqlite:///remoteCam.db', echo=True)
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
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template('base.html')

#login method
@app.route('/login', methods=['POST'])
def do_login():
    POST_USERNAME = str(request.form['username'])
    POST_PASSWORD = str(request.form['password'])
    Session = sessionmaker(bind=engine)
    s = Session()
    query = s.query(User).filter(User.username.in_([POST_USERNAME]), User.password.in_([POST_PASSWORD]) )
    result = query.first()
    if result:
        session['logged_in'] = True
    else:
        flash('wrong password!')
    return home()

# logout (NOT IMPLEMENTED ON THE WEBPAGE)
@app.route("/logout")
def logout():
    session['logged_in'] = False
    return home()

#live method, status: condition of which state on the page will be presented
@app.route('/live/<int:status>')
def live(status):
    #if not session.get('logged_in'):
        #return render_template('login.html')
    #else:
        if status:        
            return render_template('live.html', status=status)
        else:        
            return render_template('live.html', status=status)
        

# TODO has to request images from the FTP server or other DB
@app.route('/gallery')
def gallery():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template('gallery.html')

def motion_detect(firstFrame, gray, cv2):
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
        if cv2.contourArea(c) > 500:    
            return 1
        else:
            return 0
        
def save_frame(frame):
    timestr = time.strftime("%Y%m%d_%H%M%S") # Create a timestamp
    cv2.imwrite('captures/'+timestr+'.jpg',frame) #Save the curren frame


# Webcam handling

def gen(camera):
    
    firstFrame = None
    previous_time = time.time() # Get the time before motion detection
    text = "Unoccupied"
    
    while True:
        #MOTION DETECTION
        
        frame = camera.get_frame()

        # if the frame could not be grabbed, then we have reached the end
        # of the video
        if frame is None:
            break

        # resize the frame, convert it to grayscale, and blur it
        frame = imutils.resize(frame, width=500)
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray_frame = cv2.GaussianBlur(gray_frame, (21, 21), 0)
        
        # if the first frame is None, initialize it
        if firstFrame is None:
            firstFrame = gray_frame
            continue
        
        
        
        if (motion_detect(firstFrame, gray_frame, cv2) == 1):
            text = "Occupied"
            
            #Delay for saving frames
            now_time = time.time()
            
            if abs(int(now_time - previous_time)) > 2 :
                print("capture")
                previous_time = time.time()    
                save_frame(frame)
        else:
            text = "Unoccupied"
        
        #add Room status text to video feed
        cv2.putText(frame, "Room Status: {}".format(text), (10, 20),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            
        #convert the frame to jpg image and save it
        ret, jpeg = cv2.imencode('.jpg', frame)
        frame = jpeg.tobytes()
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
    
@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

app.secret_key = os.urandom(12)

