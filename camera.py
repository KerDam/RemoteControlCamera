import cv2
import datetime, time, imutils

class VideoCamera(object):
    def __init__(self):
        # Using OpenCV to capture from device 0. If you have trouble capturing
        # from a webcam, comment the line below out and use a video file
        # instead.
        self.video = cv2.VideoCapture(0)
        # If you decide to use video.mp4, you must have this file in the folder
        # as the main.py.
        # self.video = cv2.VideoCapture('video.mp4')
    
    def __del__(self):
        self.video.release()
    
    def get_jpg_frame(self):
        success, frame = self.video.read()

        # We are using Motion JPEG, but OpenCV defaults to capture raw images,
        # so we must encode it into JPEG in order to correctly display the
        # video stream.
        ret, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()
    
    def get_frame(self):
        success, frame = self.video.read()
        return frame

# Webcam handling

FRAME_SAVING_INTERVAL = 2 #seconds
MONTION_DETECTION_SENSITIVITY = 500

def get_timestamp():
    return time.strftime("%Y%m%d_%H%M%S") # Create a timestamp


def save_frame(frame, name):
    cv2.imwrite(name,frame) #Save the curren frame

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
        if cv2.contourArea(c) < MONTION_DETECTION_SENSITIVITY:    
            continue
        return 1
    return 0
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
        
        if (motion_detect(gray_frame, firstFrame, cv2) == 1):
            text = "Occupied"
            
            #Delay for saving frames
            now_time = time.time()
            
            if abs(int(now_time - previous_time)) > FRAME_SAVING_INTERVAL :
                print("capture")
                previous_time = time.time()    
                save_path = 'captures/'+get_timestamp()+'.jpg'
                save_frame(frame, save_path)
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
