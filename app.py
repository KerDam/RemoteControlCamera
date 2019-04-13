from flask import Flask, render_template, Response, session, request, session, flash, abort, redirect
from flask_nav import Nav
from flask_nav.elements import Navbar, Subgroup, Text, View
from flask_bootstrap import Bootstrap
from camera import VideoCamera
import cv2
import os
from sqlalchemy.orm import sessionmaker
from tabledef import *

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

@app.route('/login', methods=['POST'])
def do_admin_login():
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

@app.route("/logout")
def logout():
    session['logged_in'] = False
    return home()

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

#base webcam code

@app.route('/camera/<int:status>')
def camera(status):
    if status:
        #cameraOnOff(status)
        return render_template('camera.html', status=status)
    else:
        #cameraOnOff(status)
        return render_template('camera.html', status=status)
    
# Webcam handling

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
    frame = camera.get_frame()
    yield (b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
    
@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
#def cameraOnOff(status):
    #if status:
        #print("Camera ON")
    #else:
        #print("Camera OFF")

app.secret_key = os.urandom(12)
