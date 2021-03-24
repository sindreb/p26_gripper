#!/usr/bin/env python3.7

import rospy
import time
import numpy as np
from std_msgs.msg import String
import RPi.GPIO as GPIO
from pyfirmata import Arduino, util

board = Arduino('/dev/ttyACM0')
it = util.Iterator(board)
it.start()
time.sleep(0.1)
current_sense = board.analog[0]
current_sense.enable_reporting()


# Setup for GPIO on Raspberry
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD) # Use onboard GPIO on Raspberry
GPIO.setup(33, GPIO.OUT) # Set pin 33 as output
GPIO.setup(11, GPIO.OUT) # Set pin 11 as output
GPIO.setup(13, GPIO.OUT) # Set pin 13 as output

motor = GPIO.PWM(33, 500) # Set pin 33 as motor PWM output at 10000 Hz

max_opening_current = 0.01 # Maximum current for motor at opening
max_closing_current = 0.005 # Maximum current for motot at closing


def CW(speed):
    motor.stop()
    GPIO.output(11, GPIO.HIGH)
    GPIO.output(13, GPIO.LOW)
    motor.start(0)
    motor.ChangeDutyCycle(speed)
    

def CCW(speed):
    motor.stop()
    GPIO.output(11, GPIO.LOW)
    GPIO.output(13, GPIO.HIGH)
    motor.start(0)
    for dc in np.arange(0, speed, 1/speed):
        motor.ChangeDutyCycle(dc)
    #    print(dc)
    #    print(current_sense.read())
        time.sleep(0.1/speed)

def sleep(sec):
    for sleep in np.arange(0, sec, 0.2):
        current_average()
        time.sleep(0.2)
    board.analog[0].disable_reporting()    

def current_average():
    current_it = 0
    for current_count in np.arange(0, 40, 1):
        current_it += current_sense.read()
        time.sleep(0.1/40)
 
    current_avg = np.round(current_it/40, 5)
    #print(current_avg)
    return current_avg


def hold():
    motor.stop()
    GPIO.output(11, GPIO.LOW)
    GPIO.output(13, GPIO.LOW)
    motor.start(0)

def open():
    print("Opening gripper...")
    CW(5)
    current_avg = 0
    while current_sense.read() == None:
        pass

    while current_avg < max_opening_current:
        current_avg = current_average()
        print(current_avg)

    hold()

#while True:

#    open()
#    time.sleep(5)
    #CW(5)
    #for freq in np.array([100, 500, 1000, 2000, 4000, 5000, 7000, 10000, 12000, 15000, 20000]):
    #    motor.ChangeFrequency(freq)
    #    print(freq)
    #    time.sleep(5)

