from flask import Flask, render_template, Response, session, request, session, flash, abort, redirect
from imutils.video import VideoStream
from flask_nav import Nav
from flask_nav.elements import Navbar, Subgroup, Text, View
from flask_bootstrap import Bootstrap
from camera import *
import cv2
import os
from sqlalchemy.orm import sessionmaker
from tabledef import *
from multiprocessing import Process, Value
from ftp_uploader import *

import argparse, datetime, time, imutils

engine = create_engine('sqlite:///remoteCam.db', echo=True)
app = Flask(__name__)
nav = Nav(app)
Bootstrap(app)

#Uploader Parameters
NB_LOCAL_FILES_LIMIT = 5
TIME_INTERVAL_LOCAL_FILES_CHECKING = 5
SERVER_ADDRESS = "files.000webhost.com"
UPLOAD_DIR = "public_html/uploads/"
#FTP Credentials
ftp_username = "axc-agile"
ftp_pass = "axc-agile"

#-------------------------

@nav.navigation('site_navbar')
def create_navbar():
    live_view = View('Live','live',status=0) #init with OFF state of the webcam
    gallery_view = View('Gallery','gallery')
    return Navbar('RemoteCamera', live_view, gallery_view)

@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template('gallery.html')

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
    return gallery()

# logout (NOT IMPLEMENTED ON THE WEBPAGE)
@app.route("/logout")
def logout():
    session['logged_in'] = False
    return gallery()

#live method, status: condition of which state on the page will be presented
@app.route('/live/<int:status>')
def live(status):
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        if status:        
            return render_template('live.html', status=status)
        else:        
            return render_template('live.html', status=status)
        

# Requests the images to the ftp server
@app.route('/gallery', methods=['GET'])
def gallery():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        ftp = ftplib.FTP(SERVER_ADDRESS)
        ftp.login(ftp_username,ftp_pass)
        ftp.cwd(UPLOAD_DIR) 
        img_list = list_remote_files(ftp)
        ftp.quit()
        return render_template('gallery.html', img_list=img_list)
    
@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

app.secret_key = os.urandom(12)

def upload_loop():
   while True:
       if(len(list_local_files("captures/")) > NB_LOCAL_FILES_LIMIT):
            print("Start uploading..")
            ftp = ftplib.FTP(SERVER_ADDRESS)
            ftp.login(ftp_username,ftp_pass)
            ftp.cwd(UPLOAD_DIR) 
            data = Diff(list_local_files("captures/"), list_remote_files(ftp))
            os.chdir(r"captures/") 
            upload_files(ftp, data)
            log_file="log.txt"
            ftp.storbinary("STOR " + log_file, open(log_file, "rb"), 1024)
            ftp.quit()
            delete_files(data)
            os.chdir(r"..") 
       time.sleep(TIME_INTERVAL_LOCAL_FILES_CHECKING)

if __name__ == "__main__":
    p = Process(target=upload_loop)
    p.start()  
    app.run(host= '0.0.0.0')
    p.join()
