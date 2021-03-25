#!/usr/bin/env python3.7

import time
import numpy as np
import RPi.GPIO as GPIO
from pyfirmata import Arduino, util

# Setup for communication with Arduino
board = Arduino('/dev/ttyACM0') # Define device connection
it = util.Iterator(board)   # Receive data into iterator
it.start()
time.sleep(0.1)
current_sense = board.analog[0] # Define analog pin 0
current_sense.enable_reporting() # Start reporting from current_sense


# Setup for GPIO on Raspberry
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD) # Use onboard GPIO on Raspberry
GPIO.setup(33, GPIO.OUT) # Set pin 33 as output
GPIO.setup(11, GPIO.OUT) # Set pin 11 as output
GPIO.setup(13, GPIO.OUT) # Set pin 13 as output

motor = GPIO.PWM(33, 18000) # Set pin 33 as motor PWM output at 10000 Hz

max_opening_current = 0.013 # Maximum current for motor at opening
max_closing_current = 0.01 # Maximum current for motot at closing


def CW(speed):
    motor.stop()
    GPIO.output(11, GPIO.HIGH)
    GPIO.output(13, GPIO.LOW)
    motor.start(0)
    motor.ChangeDutyCycle(speed)
    

def CCW(speed):
    motor.stop()
    GPIO.output(13, GPIO.HIGH)
    GPIO.output(11, GPIO.LOW)
    motor.start(0)
    motor.ChangeDutyCycle(speed)
    

def sleep(sec):
    for sleep in np.arange(0, sec, 0.2):
        current_average()
        time.sleep(0.2)
    board.analog[0].disable_reporting()    

def current_average(): # Finds and calculates average current
    current_it = 0
    for current_count in np.arange(1, 40, 1): # 40 measurements
        current_it += current_sense.read()
        time.sleep(0.1/40) # Time between each measurement
 
    current_avg = np.round(current_it/40, 5) # Average of 40 measurement, rounded to 5 decimals
    return current_avg

def hold(): # Holds torque at the motor by brake to ground
    GPIO.output(11, GPIO.LOW)
    GPIO.output(13, GPIO.LOW)
    motor.start(0)

def open():
    print("Opening gripper...")
    CW(5)
    current_avg = 0
    current_max_count = 0
    while current_sense.read() == None: # Passes through initial None value
        pass

    while current_max_count < 3:
        if current_avg > max_opening_current:
            current_max_count += 1
    
        current_avg = current_average()
        print(current_avg)
    hold()

def close():
    print("Closing gripper...")
    CCW(5)
    current_avg = 0
    while current_sense.read() == None: # Passes through initial None value
        pass

    while current_avg < max_closing_current:
        current_avg = current_average()
        print(current_avg)
    hold()


while True:

    open()
    time.sleep(5)



    #CW(5)
    #for freq in np.array([100, 500, 1000, 2000, 4000, 5000, 7000, 10000, 12000, 15000, 20000]):
    #    motor.ChangeFrequency(freq)
    #    print(freq)
    #    time.sleep(5)

