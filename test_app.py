import cv2
import numpy as np
from app import *

def test_motion_detect_no_move():
    cap = cv2.VideoCapture('open_cv_tests/1.avi')
    detection = 5
    firstFrame = None

    # Read until video is completed
    while(cap.isOpened()):
        # Capture frame-by-frame
        ret, frame = cap.read()
        if ret == True:
            
            frame = imutils.resize(frame, width=500)
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray_frame = cv2.GaussianBlur(gray_frame, (21, 21), 0)  
            
            if firstFrame is None:
                firstFrame = gray_frame
                continue
            
            #cv2.imshow('Frame',gray_frame)
            detection = motion_detect(firstFrame, gray_frame, cv2)
            
            # Press Q on keyboard to  exit
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
    
        # Break the loop
        else: 
            break

    assert detection == None

    # When everything done, release the video capture object
    cap.release()
 
def test_motion_detect_move():
    cap = cv2.VideoCapture('open_cv_tests/2.avi')
    detection = 5
    firstFrame = None

    # Read until video is completed
    while(cap.isOpened()):
        # Capture frame-by-frame
        ret, frame = cap.read()
        if ret == True:
            
            frame = imutils.resize(frame, width=500)
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray_frame = cv2.GaussianBlur(gray_frame, (21, 21), 0)  
            
            if firstFrame is None:
                firstFrame = gray_frame
                continue
            
            #cv2.imshow('Frame',gray_frame)
            detection = motion_detect(firstFrame, gray_frame, cv2)
            
            # Press Q on keyboard to  exit
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
    
        # Break the loop
        else: 
            break

    assert detection == 1

    # When everything done, release the video capture object
    cap.release()
