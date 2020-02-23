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
import teleg
import TargetMode

serv = servoLib.SG90servo("serv", 50)
maxX = 145
minX = 50
maxY = 180
minY = 130

global threadBusiness

# def servo_thread():
# serv.business(23, 24, 0.05, maxX, minX, maxY, minY, 4, 1)


def servo_thread():
    serv.business_2(23, 24, 0.3)


# def temp_thread():
#     mlx = mlx90614.MLX90614()
#     flag = False
#     while True:
#         time.sleep(0.5)
#         temp = mlx.get_obj_temp()
#         if (temp > 27 or temp < 22):
#             # if not flag:
#             #     flag = True
#             #     serv.set_send(True)
#             x = serv.get_x()
#             y = serv.get_y()
#             print("{}:{} = {}:{} \"{}C\"".format(x, y, int(np.abs(int(18 - int(y-minY)/int(int(maxY - minY)/18)))), int(np.abs(
#                 int(int(x-minX)/int(int(maxX-minX)/19)))), temp))
#             servoLib.ImageArr[int(np.abs(int(18 - int(y-minY)/int(int(maxY - minY)/18)))), int(np.abs(
#                 int(int(x-minX)/int(int(maxX-minX)/19))))] = int(temp)
    # else:
    #     flag = False


app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')


def gen2(camera):
    """Returns a single image frame"""
    frame = camera.get_frame()
    frame = cv2.flip(frame, 1)
    tmp_arr = np.transpose(servoLib.ImageArr, (1, 0))
    for x in range(0, 9):
        for y in range(0, 9):
            if tmp_arr[x, y] < 18 or tmp_arr[x, y] > 27:
                cv2.circle(frame, (int((y+1) * 75)-5, int((x+1) * 63)-5), 10, (int(
                    255-tmp_arr[x, y]*5), 0, int(0+tmp_arr[x, y]*5)), 2)
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
        tmp_arr = np.transpose(servoLib.ImageArr, (1, 0))
        for x in range(0, 9):
            for y in range(0, 9):
                if tmp_arr[x, y] < 18 or tmp_arr[x, y] > 27:
                    cv2.circle(frame1, (int((y+1) * 75)-5, int((x+1) * 63)-5), 10, (int(
                        255-tmp_arr[x, y]*5), 0, int(0+tmp_arr[x, y]*5)), 2)
        # cv2.putText(frame1, new_date, (425, 465),
        #             cv2.FONT_HERSHEY_TRIPLEX, 1, (0, 0, 0), lineType=cv2.LINE_AA)
        ret, jpeg = cv2.imencode('.jpg', frame1)
        frame = jpeg.tobytes()
        yield (b' --frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/setXY')
def setXY():
    mlx = mlx90614.MLX90614()
    x = request.args.get("x")
    y = request.args.get("y")
    print("x = " + x)
    print("y = " + y)
    x, y = TargetMode.target(x, y)
    servo_pin_x = 23
    servo_pin_y = 24
    print("new x = " + str(x))
    print("new y = " + str(y))
    serv.servo_move_step(23, int(x), int(x))
    serv.servo_move_step(24, int(y), int(y))
    print("Temp: {}".format(mlx.get_obj_temp()))
    
    return render_template("index.html")


@app.route('/mod1')
def mod1():
    print("Toggle Telegram Mode")
    global threadBusiness
    servoLib.servoStopFlag = False
    threadBusiness.join()
    teleg.enabledFlag = not teleg.enabledFlag
    servoLib.servoStopFlag = True
    threadBusiness = threading.Thread(target=servo_thread)
    threadBusiness.start()

    print("Telegram Notify = {}".format(teleg.enabledFlag))
    return render_template("index.html")


@app.route('/mod2')
def mod2():
    print("Normal Mode")
    servoLib.servoStopFlag = True
    threadBusiness = threading.Thread(target=servo_thread)
    threadBusiness.start()
    return render_template("index.html")


@app.route('/mod3')
def mod3():
    print("TargetMode")
    servoLib.servoStopFlag = False
    threadBusiness.join()
    return render_template("index.html")


@app.route('/mod4')
def mod4():
    print("mod4")
    return render_template("index.html")


@app.route('/stop')
def stop():
    print("STOP")
    servoLib.servoStopFlag = False
    threadBusiness.join()

    return render_template("index.html")


if __name__ == '__main__':
   # global threadBusiness
    threadBusiness = threading.Thread(target=servo_thread)
    # y = threading.Thread(target=temp_thread)
    threadBusiness.start()
    # y.start()
    app.run(host='0.0.0.0', threaded=True)
    # y.join()
