#!/usr/bin/env python3
"""
# ========================= HEADER ===================================
# title             :rpiservolib.py
# description       :Part of a RpiMotorLib python 3 library for motors
# and servos to connect to a raspberry pi
# This file is for servos controlled by GPIO PWM
# author            :Gavin Lyons
# web               :https://github.com/gavinlyonsrepo/RpiMotorLib
# mail              :glyons66@hotmail.com
# python_version    :3.4.2
"""
# ========================== IMPORTS ======================
# Import the system modules needed to run rpiMotorlib.py
import sys
import time
import RPi.GPIO as GPIO
import numpy as np
from threading import Lock
import teleg
# ==================== CLASS SECTION ===============================

ImageArr = np.zeros([19, 21])
for i in range(0, 19):
    for j in range(0, 21):
        ImageArr[i, j] = int(23)


class SG90servo(object):
    """class to control a servo with GPIO PWM by raspberry pi"""

    def __init__(self, name="SG90servoX", freq=50, y_one=2, y_two=12):
        """ init method for class
        4 inputs
        (1) name, default=SG90servoX, type=string, help=name of instance
        (2) Freq, type=int, default=50,  help=control freq of servo in Hz
        (3) y_one, type=float, default = 2 ,help=pulse min duty cycle of servo % for 0 degrees
        (4) y_two type=float, default = 12, help=pulse max duty cycle of servo % for 180 degrees
          """
        self.mutex = Lock()
        self.name = name
        self.freq = freq
        self.y_one = y_one
        self.y_two = y_two
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        self.curr_x = 130
        self.curr_y = 130
        self.global_delay = 0.01
        self.delay_switch = True  # True is default, False is global
        self.send_msg = False

    def set_x(self, val):
        with self.mutex:
            self.curr_x = val

    def set_y(self, val):
        with self.mutex:
            self.curr_y = val

    def get_x(self):
        with self.mutex:
            return self.curr_x

    def get_y(self):
        with self.mutex:
            return self.curr_y

    def set_delay(self, val):
        with self.mutex:
            self.delay_switch = False
            self.global_delay = val

    def reset_delay(self):
        with self.mutex:
            self.delay_switch = True

    def get_delay(self):
        with self.mutex:
            return self.global_delay

    def get_delay_switch(self):
        with self.mutex:
            return self.delay_switch

    def set_send(self, val):
        with self.mutex:
            self.send_msg = val

    def get_send(self):
        with self.mutex:
            return self.send_msg

    def business(self, servo_pin_x, servo_pin_y, stepdelay=0.08,
                 maxX=135,
                 minX=70,
                 maxY=160,
                 minY=130, stepsize_x=5, stepsize_y=3, initdelay=1):
        GPIO.setup(servo_pin_x, GPIO.OUT)
        GPIO.setup(servo_pin_y, GPIO.OUT)
        time.sleep(initdelay)
        pwm_servo_y = GPIO.PWM(servo_pin_y, self.freq)
        pwm_servo_x = GPIO.PWM(servo_pin_x, self.freq)
        try:
            start_x = self.convert_from_degree(minX)
            start_y = self.convert_from_degree(minY)
            pwm_servo_y.start(start_y)
            pwm_servo_x.start(start_x)
            flag_y = True
            flag_x = True
            while True:
                if flag_x:
                    for x in range(minX, maxX, stepsize_x):
                        if flag_y:
                            for y in range(minY, maxY, stepsize_y):
                                self.set_y(y)
                                pwm_servo_y.ChangeDutyCycle(
                                    self.convert_from_degree(y))
                                # if self.get_delay_switch():
                                time.sleep(stepdelay)
                                # else:
                                #     time.sleep(self.get_delay())
                        else:
                            for y in range(maxY, minY, -stepsize_y):
                                self.set_y(y)
                                pwm_servo_y.ChangeDutyCycle(
                                    self.convert_from_degree(y))
                                # if self.get_delay_switch():
                                time.sleep(stepdelay)
                                # else:
                                #     time.sleep(self.get_delay())
                        self.set_x(x)
                        # if np.abs(x-(maxX-minX)/2) > 40
                        #     stepsize_x
                        pwm_servo_x.ChangeDutyCycle(
                            self.convert_from_degree(x))
                        flag_y = not flag_y
                else:
                    for x in range(maxX, minX, -stepsize_x):
                        if flag_y:
                            for y in range(minY, maxY, stepsize_y):
                                self.set_y(y)
                                pwm_servo_y.ChangeDutyCycle(
                                    self.convert_from_degree(y))
                                # if self.get_delay_switch():
                                time.sleep(stepdelay)
                                # else:
                                #     time.sleep(self.get_delay())
                        else:
                            for y in range(maxY, minY, -stepsize_y):
                                self.set_y(y)
                                pwm_servo_y.ChangeDutyCycle(
                                    self.convert_from_degree(y))
                                # if self.get_delay_switch():
                                time.sleep(stepdelay)
                                # else:
                                #     time.sleep(self.get_delay())
                        self.set_x(x)
                        pwm_servo_x.ChangeDutyCycle(
                            self.convert_from_degree(x))
                        flag_y = not flag_y
                flag_x = not flag_x
                if(self.get_send()):
                    self.set_send(False)
                    teleg.sendPhoto(teleg.bot)
        except KeyboardInterrupt:
            print("CTRL-C: RpiServoLib: Terminating program.")
        finally:
            pwm_servo_x.stop()
            pwm_servo_y.stop()
            GPIO.output(servo_pin_y, False)
            GPIO.output(servo_pin_x, False)

    def convert_from_degree(self, degree):
        """ converts degrees to duty cycle percentage , takes in degree
        returns duty cycle float"""
        x_two = 180
        x_one = 0
        slope = (self.y_two-self.y_one)/(x_two-x_one)
        duty_cycle = slope*(degree-x_one) + self.y_one
        return duty_cycle


def importtest(text):
    """import print test statement"""
    pass
    # print(text)

# ===================== MAIN ===============================


if __name__ == '__main__':
    importtest("main")
else:
    importtest("Imported {}".format(__name__))


# ===================== END ===============================
