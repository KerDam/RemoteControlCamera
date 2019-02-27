from flask import Flask
from flask import render_template
app = Flask(__name__)


@app.route('/')
def hello_world():
    return '<h1>Hello, World!</h1>'


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
