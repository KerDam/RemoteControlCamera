from flask import Flask, render_template, Response
from camera import VideoCamera
import cv2

app = Flask(__name__)


global cam

@app.route('/')
def hello_world():
    return '<h1>Hello, World!</h1>'


@app.route('/camera/<int:status>')
def camera(status):
    if status:
        #cameraOnOff(status)
        return render_template('camera.html', status=status)
    else:
        #cameraOnOff(status)
        return render_template('camera.html', status=status)

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

#if __name__ == '__main__':
        #app.run(host='0.0.0.0', debug=True, threaded=True)
