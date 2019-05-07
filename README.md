# Remote Controlled Camera

## Description
This project aim is to provide a remote controlled camera. With this, you are able to turn on and off your camera from your web browsers and it will detect any movement on the stream. Once motion is detected, a screenshot and informations related to the date are sent to a web server and you can then access it from the website.

## SYSTEM PREREQUISITES

_In order to run our application, you will need to download and install the following tools:_

- A machine running with Ubuntu where the other tools have to be installed
- Python
- Flask
- OpenCV
- SQLAlchemy

Installation of Python libraries : 

    sudo pip install flask flask-nav flask-bootstrap sqlalchemy

OpenCV install script : https://github.com/milq/milq/blob/master/scripts/bash/install-opencv.sh

_You will also need a webcam._

## Usage

Start the server with :
    python app.py

Login on 127.0.0.1:5000 port (local machine)
Username : agile
Password : agile

 - Home tab:
 - Live tab: Click on the on/off button to turn on/off the webcam. The live stream will be displayed and the motion detection will be performed as well.
 - Gallery tab: Displays the screenshots taken by the motion detection with timestamp.

## Credits


Seid Issa, Bonnie Trexler, Nuno Realista, Damien Farce, Thibault Gainche, Changlu Guo, Alex Colleux, Maxime Melet


## Build status

![Build status](https://travis-ci.com/KerDam/RemoteControlCamera.svg?token=qxfBb92XCJLsFBjvpayK&branch=master)


https://travis-ci.com/KerDam/RemoteControlCamera

https://codeclimate.com/github/KerDam/RemoteControlCamera
