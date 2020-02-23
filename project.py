from flask import Flask, render_template, Response, request
from camera import VideoCamera
import servoLib
import cv2
import numpy as np
import threading
import RPi.GPIO as GPIO
from datetime import datetime

def servo_thread():
    serv = servoLib.SG90servo("serv", 50)
    maxX = 145
    minX = 50
    maxY = 180
    minY = 130
    serv.business(23, 24, 0.01, maxX, minX, maxY, minY, 1 , 1)

app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')

def gen(camera):
    while True:
        frame1 = camera.get_frame()
        frame1 = cv2.rotate(frame1, 1)
        for x in range(0, 19):
            for y in range(0, 21):
                if servoLib.ImageArr[x,y] < 18 or servoLib.ImageArr[x,y] > 27:
                    cv2.circle(frame1, (int(((y+1) * 70)/2), int(((x+1) * 40)/2)), 10, (int(255-servoLib.ImageArr[x,y]*5), 0, int(0+servoLib.ImageArr[x,y]*5)), 2)
        new_date = datetime.now().strftime("%H:%M:%S:%f")[:-3]
        cv2.putText(frame1, new_date, (425, 465), cv2.FONT_HERSHEY_TRIPLEX, 1, (0, 0, 0), lineType=cv2.LINE_AA)        
        ret, jpeg = cv2.imencode('.jpg', frame1)
        frame = jpeg.tobytes()
        yield (b' --frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    x = threading.Thread(target=servo_thread)
    x.start()
    app.run(host='0.0.0.0', debug=False)
    x.join()
