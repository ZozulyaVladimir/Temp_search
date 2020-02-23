from flask import Flask, render_template, Response, request
from camera import VideoCamera
import servoLib
import cv2
import numpy as np
import threading
import RPi.GPIO as GPIO
from datetime import datetime
import mlx90614
import time
import sys
import teleg
import math

serv = servoLib.SG90servo("serv", 50)
maxX = 145
minX = 50
maxY = 180
minY = 130


def servo_thread():
    serv.business(23, 24, 0.05, maxX, minX, maxY, minY, 4, 1)


def temp_thread():
    mlx = mlx90614.MLX90614()
    flag = False
    while True:
        time.sleep(0.5)
        temp = mlx.get_obj_temp()
        if (temp > 27 or temp < 22):
            # if not flag:
            #     flag = True
            #     serv.set_send(True)
            x = serv.get_x()
            y = serv.get_y()
            print("{}:{} = {}:{} \"{}C\"".format(x, y, int(np.abs(int(18 - int(y-minY)/int(int(maxY - minY)/18)))), int(np.abs(
                int(int(x-minX)/int(int(maxX-minX)/19)))), temp))
            servoLib.ImageArr[int(np.abs(int(18 - int(y-minY)/int(int(maxY - minY)/18)))), int(np.abs(
                int(int(x-minX)/int(int(maxX-minX)/19))))] = int(temp)
        # else:
        #     flag = False


app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')


def gen2(camera):
    """Returns a single image frame"""
    frame = camera.get_frame()
    frame = cv2.flip(frame,1)
    for x in range(0, 19):
        for y in range(0, 21):
            if servoLib.ImageArr[x, 20- y] < 22 or servoLib.ImageArr[x, 20 - y] > 27:
                if x == 0:
                    cv2.circle(frame, (int(((y+1) * 50)/2), 460 ), 10, (int(
                    0+servoLib.ImageArr[x, y]*5), 0, int(255-servoLib.ImageArr[x, y]*5)), 2)
                elif x == 1:
                    cv2.circle(frame, (int(((y+1) * 50)/2), 415 ), 10, (int(
                    0+servoLib.ImageArr[x, y]*5), 0, int(255-servoLib.ImageArr[x, y]*5)), 2)
                elif x == 2:
                    cv2.circle(frame, (int(((y+1) * 50)/2), 370 ), 10, (int(
                    0+servoLib.ImageArr[x, y]*5), 0, int(255-servoLib.ImageArr[x, y]*5)), 2)
                elif x == 3:
                    cv2.circle(frame, (int(((y+1) * 50)/2), 330 ), 10, (int(
                    0+servoLib.ImageArr[x, y]*5), 0, int(255-servoLib.ImageArr[x, y]*5)), 2)
                elif x == 4:
                    cv2.circle(frame, (int(((y+1) * 50)/2), 290 ), 10, (int(
                    0+servoLib.ImageArr[x, y]*5), 0, int(255-servoLib.ImageArr[x, y]*5)), 2)
                elif x == 5:
                    cv2.circle(frame, (int(((y+1) * 50)/2), 260 ), 10, (int(
                    0+servoLib.ImageArr[x, y]*5), 0, int(255-servoLib.ImageArr[x, y]*5)), 2)
                elif x == 6:
                    cv2.circle(frame, (int(((y+1) * 50)/2), 230 ), 10, (int(
                    0+servoLib.ImageArr[x, y]*5), 0, int(255-servoLib.ImageArr[x, y]*5)), 2)
                elif x == 7:
                    cv2.circle(frame, (int(((y+1) * 50)/2), 200 ), 10, (int(
                    0+servoLib.ImageArr[x, y]*5), 0, int(255-servoLib.ImageArr[x, y]*5)), 2)
                elif x == 8:
                    cv2.circle(frame, (int(((y+1) * 50)/2), 180 ), 10, (int(
                    0+servoLib.ImageArr[x, y]*5), 0, int(255-servoLib.ImageArr[x, y]*5)), 2)
                elif x == 9:
                    cv2.circle(frame, (int(((y+1) * 50)/2), 160 ), 10, (int(
                    0+servoLib.ImageArr[x, y]*5), 0, int(255-servoLib.ImageArr[x, y]*5)), 2)
                elif x == 10:
                    cv2.circle(frame, (int(((y+1) * 50)/2), 140), 10, (int(
                    0+servoLib.ImageArr[x, y]*5), 0, int(255-servoLib.ImageArr[x, y]*5)), 2)
                elif x == 11:
                    cv2.circle(frame, (int(((y+1) * 50)/2), 120 ), 10, (int(
                    0+servoLib.ImageArr[x, y]*5), 0, int(255-servoLib.ImageArr[x, y]*5)), 2)
                elif x == 12:
                    cv2.circle(frame, (int(((y+1) * 50)/2), 100 ), 10, (int(
                    0+servoLib.ImageArr[x, y]*5), 0, int(255-servoLib.ImageArr[x, y]*5)), 2)
                elif x == 13:
                    cv2.circle(frame, (int(((y+1) * 50)/2), 85 ), 10, (int(
                    0+servoLib.ImageArr[x, y]*5), 0, int(255-servoLib.ImageArr[x, y]*5)), 2)
                elif x == 14:
                    cv2.circle(frame, (int(((y+1) * 50)/2), 70 ), 10, (int(
                    0+servoLib.ImageArr[x, y]*5), 0, int(255-servoLib.ImageArr[x, y]*5)), 2)
                elif x == 15:
                    cv2.circle(frame, (int(((y+1) * 50)/2), 60 ), 10, (int(
                    0+servoLib.ImageArr[x, y]*5), 0, int(255-servoLib.ImageArr[x, y]*5)), 2)
                elif x == 16:
                    cv2.circle(frame, (int(((y+1) * 50)/2), 50 ), 10, (int(
                    0+servoLib.ImageArr[x, y]*5), 0, int(255-servoLib.ImageArr[x, y]*5)), 2)
                elif x == 17:
                    cv2.circle(frame, (int(((y+1) * 50)/2), 40 ), 10, (int(
                    0+servoLib.ImageArr[x, y]*5), 0, int(255-servoLib.ImageArr[x, y]*5)), 2)
                elif x == 18:
                    cv2.circle(frame, (int(((y+1) * 50)/2), 30)  , 10, (int(
                    0+servoLib.ImageArr[x, y]*5), 0, int(255-servoLib.ImageArr[x, y]*5)), 2)
                elif x == 19:
                    cv2.circle(frame, (int(((y+1) * 50)/2), 20) , 10, (int(
                    0+servoLib.ImageArr[x, y]*5), 0, int(255-servoLib.ImageArr[x, y]*5)), 2)
    rotated = cv2.flip(frame, 1)
    rotated = cv2.rotate(rotated, 1)
    yield cv2.imencode('.jpg', rotated)[1].tobytes()


@app.route('/image.jpg')
def image():
    """Returns a single current image for the webcam"""
    return Response(gen2(VideoCamera()), mimetype='image/jpeg')


def gen(camera):
    while True:
        frame1 = camera.get_frame()
        # time.sleep(0.1)
        frame1 = cv2.rotate(frame1, 1)
        for x in range(0, 19):
            for y in range(0, 21):
                if servoLib.ImageArr[x, y] < 18 or servoLib.ImageArr[x, y] > 27:
                    cv2.circle(frame1, (int(((y+1) * 70)/2), int(((x+1) * 40)/2)), 10, (int(
                        255-servoLib.ImageArr[x, y]*5), 0, int(0+servoLib.ImageArr[x, y]*5)), 2)
        new_date = datetime.now().strftime("%H:%M:%S:%f")[:-3]
        cv2.putText(frame1, new_date, (425, 465),
                    cv2.FONT_HERSHEY_TRIPLEX, 1, (0, 0, 0), lineType=cv2.LINE_AA)
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
    y = threading.Thread(target=temp_thread)
    x.start()
    y.start()
    app.run(host='0.0.0.0', threaded=True)
    y.join()
    x.join()
