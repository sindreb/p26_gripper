#!/usr/bin/env python

import rospy
from std_msgs.msg import String, Int64, Float32

pub = rospy.Publisher('p26_lefty/gripper', Int64, queue_size=10)

def grip_procedure(data):
    global actuation
    actuation = data.data

def open_grip():
    #Opening gripper
    gripper_pos = 1 #1 open, 2 closed
    rospy.loginfo("Gripper open")
    pub.publish(gripper_pos)

def close_grip():
    #Closing gripper
    gripper_pos = 2 #1 open, 2 closed
    rospy.loginfo("Gripper closed")
    pub.publish(gripper_pos)

def main():

    rospy.init_node('gripper', anonymous=True)
    rate = rospy.Rate(10)
    rospy.Subscriber("p26_lefty/gripper", Int64, grip_procedure)
    rospy.loginfo("Gripper ready for input...")
    rospy.wait_for_message("p26_lefty/gripper", Int64, timeout=None)

    if actuation == 1:
        rospy.loginfo("Opening gripper...")
        rospy.sleep(2)
        open_grip()

    elif actuation == 2:
        rospy.loginfo("Closing gripper...")
        rospy.sleep(2)
        close_grip()

    elif actuation != 1 or actuation != 2:
        rospy.loginfo("Malfunction")


while True:
    main()