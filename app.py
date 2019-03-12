from flask import Flask, render_template
from flask_nav import Nav
from flask_nav.elements import Navbar, Subgroup, Text, View
from flask_bootstrap import Bootstrap

app = Flask(__name__)
nav = Nav(app)
Bootstrap(app)

@nav.navigation('site_navbar')
def create_navbar():
    home_view = View('Home', 'home')
    live_view = View('Live','live')
    gallery_view = View('Gallery','gallery')
    return Navbar('RemoteCamera', home_view, live_view, gallery_view)

@app.route('/')
def home():
    return render_template('base.html')

@app.route('/live')
def live():
    return render_template('hello.html')

@app.route('/gallery')
def gallery():
    return render_template('hello.html')

@app.route('/camera/<int:status>')
def camera(status):
    if status:
        cameraOnOff(status)
        return render_template('camera.html', status=status)
    else:
        cameraOnOff(status)
        return render_template('camera.html', status=status)

def cameraOnOff(status):
    if status:
        print("Camera ON")
    else:
        print("Camera OFF")
